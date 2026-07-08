
import os
from natsort import natsorted
from scipy.io import loadmat


# Get Data
eeg_data_path = "data/EEG"
aud_data_path = "data/AUDIO"
eeg_files = os.listdir(eeg_data_path)
eeg_files = natsorted(eeg_files)
audio_files = os.listdir(aud_data_path)

subject_path = os.path.join(eeg_data_path, eeg_files[0])


def load_subject(subject_path):
    mat_subject = loadmat(subject_path)
    print(mat_subject.keys())
