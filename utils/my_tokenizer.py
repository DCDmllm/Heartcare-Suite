import torch
from torch import nn
import torch.nn.functional as F
from torch.nn import Module

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
        seq_length = 500,
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
        # ar_layers = 2,
        enc_kwargs: dict = dict(),
        dec_kwargs: dict = dict(),
        vq_kwargs: dict = dict()
    ):
        super().__init__()
        self.seq_length = seq_length
        self.patch_size = patch_size
        
        self.dim_patch = channels * patch_size
        self.num_tokens = seq_length // patch_size
        self.num_latent_tokens = int(self.num_tokens * latent_ratio)

        self.latents = nn.Parameter(torch.zeros(self.num_latent_tokens, dim))
        self.mask_tokens = nn.Parameter(torch.zeros(self.num_tokens, dim))
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

    @torch.no_grad()
    def tokenize(self, sequence):
        return self.forward(sequence, return_codebook_ids = True)

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
        
    def predict(self, tokens, ar_context):
        num_pred_tokens = self.num_tokens
        for _ in range(num_pred_tokens):
            context = tokens[:, -ar_context:, :]
            next_token = self.ar_predictor(context)[0][:, -1:]
            tokens = torch.cat([tokens, next_token], dim=1)
        
        pred_tokens = tokens[:, self.num_tokens:, :]
        return pred_tokens

    def forward(
        self,
        sequence,
        return_codebook_ids = False,
        return_recon_sequence = False,
        predict = False,
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
        quantized, indices, _ = self.vq(latents)

        # whether to early return
        if return_codebook_ids:
            return indices

        recon_sequence = self.decode(quantized)[:, :, :orig_sequence.shape[2]]

        # reconstruction loss
        recon_loss = F.mse_loss(recon_sequence, orig_sequence)

        if predict:
            pred_sequence = self.tokens_to_sequence(tokens[:, self.num_tokens:, :])
            return recon_loss, recon_sequence, pred_sequence

        if not return_recon_sequence:
            return recon_loss

        return recon_loss, recon_sequence