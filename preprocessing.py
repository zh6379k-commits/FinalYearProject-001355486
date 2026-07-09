import numpy as np
from mne.filter import filter_data
from mne.filter import resample as mne_resample
from scipy.signal import gammatone, lfilter
from scipy.stats import zscore

low_bandpass = 0.5
high_bandpass = 32.0

def eeg_preproc(eeg, eeg_sr, target_sr):
                  
    # Band-Pass Filtering              
    eeg_out = filter_data(
        eeg, eeg_sr, low_bandpass, high_bandpass, 
        method="fir", phase="zero", verbose="CRITICAL",
    )

    # Downsampling
    eeg_out = mne_resample(eeg_out, target_sr, eeg_sr, verbose="CRITICAL")

    # Re-Referencing To Average
    eeg_out = eeg_out - eeg_out.mean(axis=0, keepdims=True)

    # Zero-Centering
    eeg_out = zscore(eeg_out, axis=None)

    return eeg_out


def aud_preproc(aud, aud_sr, target_sr):
    aud = aud.astype(float)
    sr1 = 8000
    sr2 = 128
    freqs = np.array([178.7, 250.3, 334.5, 433.5, 549.9, 686.8, 847.7, 1036.9, 1259.3, 1520.9, 1828.4, 2190.0, 2615.1, 3114.9, 3702.6])
    power_law = 0.6

    # Resample for Filter Bank
    aud_out = filter_data(aud, aud_sr, None, sr1 / 2, verbose="CRITICAL")
    aud_out = mne_resample(aud_out, sr1, aud_sr, verbose="CRITICAL")

    # Gammatone Filter Bank & Compression
    subband_envelopes = []
    for f in freqs:
        b, a = gammatone(freq=f, ftype="fir", order=4, fs=sr1)
        subband = np.real(lfilter(b, a, aud_out))
        subband_envelopes.append(np.abs(subband) ** power_law)
    subband_envelopes = np.array(subband_envelopes)

    # Sum Subbands
    envelope = subband_envelopes.sum(axis=0)

    # Downsample
    envelope = mne_resample(envelope, sr2, sr1, verbose="CRITICAL")
    envelope = filter_data(envelope, sr2, low_bandpass, high_bandpass, verbose="CRITICAL")
    envelope = mne_resample(envelope, target_sr, sr2, verbose="CRITICAL")
    envelope = zscore(envelope)

    return envelope


def preproc(eeg, aud, eeg_sr, aud_sr, target_sr):
    
    # Preprocess EEG
    eeg_out = eeg_preproc(eeg, eeg_sr, target_sr)

    # Preprocess Audio
    aud_out = [
        aud_preproc(aud_stream, aud_sr, target_sr) for aud_stream, aud_sr in zip(aud, aud_sr)
    ]

    # Align Lengths
    min_len = min(eeg_out.shape[1], min(aud.shape[0] for aud in aud_out))
    eeg_out = eeg_out[:, :min_len]
    aud_out = np.array([aud[:min_len] for aud in aud_out])

    return eeg_out, aud_out
