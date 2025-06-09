import numpy as np
import wfdb
import neurokit2 as nk
import scipy.signal
from math import gcd

def resample(ecg, original_rate, target_rate):
    factor = gcd(original_rate, target_rate)
    up = target_rate // factor
    down = original_rate // factor
    ecg_resampled = scipy.signal.resample_poly(ecg, up, down)
    return ecg_resampled

def max_quality(quality, length):
    cumsum = np.cumsum(quality)
    cumsum = np.insert(cumsum, 0, 0)

    max_avg = -np.inf
    max_start = 0

    for start in range(len(quality) - length + 1):
        end = start + length
        window_sum = cumsum[end] - cumsum[start]
        avg = window_sum / length
        if avg > max_avg:
            max_avg = avg
            max_start = start

    return max_start

def process_ecg(ecg, seq_length=None, sampling_rate=250):
    quality = None
    if not seq_length:
        seq_length = ecg.shape[1]
    for sig in range(ecg.shape[0]):
        try:
            quality = nk.ecg_quality(ecg[sig, :], sampling_rate=sampling_rate)
            break
        except Exception as e:
            continue

    if quality is None:
        start = int((ecg.shape[1] - seq_length) / 2)
    else:
        start = max_quality(quality, seq_length)

    return ecg[:, start:start+seq_length]

def normalize(X):
    X_mean = np.mean(X, axis=-1, keepdims=1)
    X_std = np.std(X, axis=-1, keepdims=1)
    X_norm = (X - X_mean) / (X_std + 1e-6)
    return X_norm

def load_raw_data(df, path, sampling_rate, seq_length=2000, target_rate=250):
    data = []
    filename = df.filename_hr
    for f in filename:
        sample, _ = wfdb.rdsamp(path+f)
        channel = []
        for col in range(sample.shape[1]):
            ecg = sample[:, col]
            if sampling_rate != target_rate:
                ecg_resampled = resample(ecg, original_rate=sampling_rate, target_rate=target_rate)
            ecg_cleaned = nk.ecg_clean(ecg_resampled, sampling_rate=target_rate)
            channel.append(ecg_cleaned)
        
        X = np.array(channel, dtype=np.float32)
        X = process_ecg(X, seq_length=seq_length, sampling_rate=target_rate)
        norm = normalize(X)
        data.append(norm)

    data = np.array(data, dtype=np.float32)
    return data

def load_raw_ekg_data(df, path, seq_length, sampling_rate, target_rate=250):
    data = []
    filename = df.filename_hr
    for f in filename:
        sample, _ = wfdb.rdsamp(path+f)
        channel = []
        for col in range(sample.shape[1]):
            ecg = sample[:, col]
            if sampling_rate != target_rate:
                ecg_resampled = resample(ecg, original_rate=sampling_rate, target_rate=target_rate)
            ecg_cleaned = nk.ecg_clean(ecg_resampled, sampling_rate=target_rate)
            channel.append(ecg_cleaned)
        
        X = np.array(channel, dtype=np.float32)
        X = process_ecg(X, seq_length=seq_length, sampling_rate=target_rate)
        norm = normalize(X)
        data.append(norm)

    data = np.array(data, dtype=np.float32)
    return data