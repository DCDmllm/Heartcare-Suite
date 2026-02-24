sampling_rate = 500
target_rate = 250
seq_seconds = 4
patch_size = 25
latent_ratio = 0.5
channels = 12
codebook_size = 512
residual_levels = 2
signal_dim = 128
seq_length = int(target_rate * seq_seconds)
total_length = int(seq_length * (1 + latent_ratio))

signal_cfg = dict(
    dim=signal_dim,
    seq_length=seq_length,
    patch_size=patch_size,
    channels=channels,
    latent_ratio=latent_ratio,
    enc_depth=6,
    enc_heads=8,
    enc_dim_head=64,
    dec_depth=6,
    dec_heads=8,
    dec_dim_head=64,
    codebook_size=codebook_size,
    max_length_for_pred=seq_length*2,
    vq_kwargs={'residual_levels': residual_levels}
)

beat_config = f"level_{residual_levels}_code_{codebook_size}_len_{seq_length}_ratio_{latent_ratio}"
beat_dir = f"beat/{beat_config}"
beat_ckpt_dir = f"{beat_dir}/ckpt"
tokenizer_path = f"{beat_dir}/tokenizer.pth"
full_data_path = f"data/records250/records250.npy"
processed_data_path = f"data/records250/records250_len_{seq_length}_ratio_{latent_ratio}.npy"

joint_ckpt_dir = f"{beat_dir}_joint/ckpt"
ekg_npy_path = f"data/ekg/ekg_signal"
ekg_img_path = f"data/ekg/ekg_img"

QA_TYPES = ['DiagnosisClosedQA', 'DiagnosisOpenQA',
        'WaveformClosedQA', 'WaveformOpenQA',
        'RhythmClosedQA', 'RhythmOpenQA',
        'ReportGeneration', 'SignalForecasting']
original_model = "phi-3"
original_model_dir = f"model/{original_model}/original"
my_model_dir = f"model/{original_model}/{beat_config}"
qa_dir = "data/qa_dataset"