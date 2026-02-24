import torch
from torch import nn
import torch.nn.functional as F
from torch.nn import Module
import numpy as np

from einops.layers.torch import Rearrange
from einops import repeat, pack, unpack

from utils.my_residual_vector_quantize import VectorQuantize as VQ
from x_transformers import Encoder

# tokenizer
class Tokenizer(Module):
    def __init__(
        self,
        *,
        dim = 128,
        seq_length = 1000,
        patch_size = 25,
        channels = 12,
        latent_ratio = 0.5,
        enc_depth = 6,
        enc_heads = 8,
        enc_dim_head = 64,
        dec_depth = 6,
        dec_heads = 8,
        dec_dim_head = 64,
        codebook_size = 256,
        max_length_for_pred = 1000,
        enc_kwargs: dict = dict(),
        dec_kwargs: dict = dict(),
        vq_kwargs: dict = dict()
    ):
        super().__init__()
        self.seq_length = seq_length
        self.patch_size = patch_size
        self.channels = channels
        
        self.dim_patch = channels * patch_size
        self.num_tokens = seq_length // patch_size
        self.num_latent_tokens = int(self.num_tokens * latent_ratio)

        self.latent_ratio = latent_ratio
        self.latents = nn.Parameter(torch.zeros(self.num_latent_tokens, dim))
        self.mask_tokens = nn.Parameter(torch.zeros(self.num_tokens, dim))
        self.max_length_for_pred = max_length_for_pred

        nn.init.normal_(self.latents, std=0.02)
        nn.init.normal_(self.mask_tokens, std=0.02)

        self.pos_emb = nn.Embedding(1024, dim)
        nn.init.normal_(self.pos_emb.weight, std=0.02)

        self.sequence_to_tokens = nn.Sequential(
            Rearrange('b c (n p) -> b n (c p)', p=patch_size),
            nn.Linear(self.dim_patch, dim)
        )
        
        self.encoder = Encoder(
            dim = dim,
            depth = enc_depth,
            heads = enc_heads,
            attn_dim_head = enc_dim_head,
            **enc_kwargs
        )

        self.vq = VQ(
            dim = dim,
            codebook_dim = dim,
            codebook_size = codebook_size,
            codebook_diversity_loss_weight=0.3,
            **vq_kwargs
        )

        self.decoder = Encoder(
            dim = dim,
            depth = dec_depth,
            heads = dec_heads,
            attn_dim_head = dec_dim_head,
            **dec_kwargs
        )

        self.tokens_to_sequence = nn.Sequential(
            nn.Linear(dim, self.dim_patch),
            Rearrange('b n (c p) -> b c (n p)', p=patch_size)
        )

    def preprocess_sequence(self, sequence):
        b, c, t = sequence.shape
        segments, pad_lens = [], []
        start = t
        while start > 0:
            end = max(0, start - self.seq_length)
            seg = sequence[..., end:start]
            pad = max(0, self.seq_length - seg.shape[-1])
            seg = F.pad(seg, (pad, 0))
            segments.append(seg)
            pad_lens.append(pad)
            start -= self.seq_length
        return segments[::-1], pad_lens[::-1]
    
    def preprocess_sequence(self, sequence):
        b, c, t = sequence.shape
        segments, pad_lens = [], []
        start = t

        if t == 0:
            pad = self.seq_length
            seg = torch.zeros(b, c, self.seq_length, device=sequence.device, dtype=sequence.dtype)
            return [seg], [pad]

        while start > 0:
            end = max(0, start - self.seq_length)
            seg = sequence[..., end:start]
            pad = max(0, self.seq_length - seg.shape[-1])
            seg = F.pad(seg, (pad, 0))
            segments.append(seg)
            pad_lens.append(pad)
            start -= self.seq_length

        if len(segments) == 0:
            seg = F.pad(sequence, (self.seq_length - t, 0))
            segments = [seg]
            pad_lens = [self.seq_length - t]

        return segments[::-1], pad_lens[::-1]

    def tokenize(self, sequence):
        with torch.no_grad():
            _, _, _, indices = self.forward(sequence, return_codebook_ids = True)
            return indices

    def codebook_ids_to_sequence(self, token_ids):
        codes = self.vq.get_output_from_indices(token_ids)
        return self.decode(codes)

    def decode(self, latents):
        batch = latents.shape[0]
        positions = torch.arange(self.num_tokens, device=latents.device)
        pos_emb = self.pos_emb(positions).unsqueeze(0).expand(batch, -1, -1)
        
        mask_tokens = repeat(pos_emb, 'b n d -> b n d', b=batch)    
        tokens, mask_packed_shape = pack([mask_tokens, latents], 'b * d')

        # decode
        tokens = self.decoder(tokens)
        tokens, _ = unpack(tokens, mask_packed_shape, 'b * d')

        # tokens to sequence patches
        recon = self.tokens_to_sequence(tokens)
        return recon
        
    def predict(self, tokens, num_pred_tokens):
        pred_tokens = []
        steps = (num_pred_tokens + self.num_latent_tokens - 1) // self.num_latent_tokens
        context = tokens
        for _ in range(steps):
            length_for_pred = max(context.shape[1], self.max_length_for_pred)
            next_token = self.encoder(context[:, -length_for_pred:, :])[:, -1:, :]
            pred_tokens.append(next_token)
            context = torch.cat([context, next_token], dim=1)
        pred_tokens = torch.cat(pred_tokens, dim=1)[:, :num_pred_tokens, :]
        return pred_tokens

    def forward_segment(
        self,
        sequence,
        # return_sequence = True
    ):
        batch = sequence.shape[0]
        orig_sequence = sequence

        # sequence patches to tokens
        tokens = self.sequence_to_tokens(sequence)

        positions = torch.arange(tokens.size(1), device=tokens.device)
        pos_emb = self.pos_emb(positions)  # [n, d]
        pos_emb = pos_emb.unsqueeze(0).expand(batch, -1, -1)  # [b, n, d]
        tokens = tokens + pos_emb

        # concat latents
        latents = repeat(self.latents, 'l d -> b l d', b = batch)
        tokens, latents_packed_shape = pack([tokens, latents], 'b * d')

        # encoder
        tokens = self.encoder(tokens)

        # slice out latents and pass through vq as codes
        # this is the important line of code and main proposal of the paper
        _, latents = unpack(tokens, latents_packed_shape, 'b * d')

        # vq - usually tokens here, but they do the latents
        quantized, indices, vq_loss = self.vq(latents)

        # reconstruction loss
        recon_sequence = self.decode(quantized)[:, :, :orig_sequence.shape[2]]

        # if not return_sequence:
        #     return recon_loss

        pred_sequence = self.tokens_to_sequence(tokens[:, self.num_tokens:, :])

        return recon_sequence, pred_sequence, indices, quantized, vq_loss
        
    def forward(
        self,
        sequence,
        return_quant = False,
        # return_sequence = True
    ):    
        segments, pad_lens = self.preprocess_sequence(sequence)
        recon_sequence, pred_sequence, indices, quantized = [], [], [], []
        vq_avg_loss = []
        for seg in segments:
            recon, pred, idx, q, vq_loss = self.forward_segment(seg)
            recon_sequence.append(recon)
            pred_sequence.append(pred)
            indices.append(idx)
            quantized.append(q)
            vq_avg_loss.append(vq_loss)
        recon_cat = torch.cat(recon_sequence, dim=-1)
        pred_cat = torch.cat(pred_sequence, dim=-1)
        indices_cat = torch.cat(indices, dim=-1)
        quantized_cat = torch.cat(quantized, dim=-1)
        recon_loss = F.mse_loss(recon_cat, sequence)
        vq_avg_loss = torch.stack(vq_avg_loss).mean()
    
        if return_quant:
            return recon_loss, vq_avg_loss, recon_cat, pred_cat, indices_cat, quantized_cat
        else:
            return recon_loss, vq_avg_loss, recon_cat, pred_cat, indices_cat