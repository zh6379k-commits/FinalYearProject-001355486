
import os


# Get Data
eeg_data_path = "data/EEG"
aud_data_path = "data/AUDIO"
eeg_files = os.listdir(eeg_data_path)
audio_files = os.listdir(aud_data_path)


print(eeg_files)
print(audio_files)
