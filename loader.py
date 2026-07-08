
import os
from natsort import natsorted
from scipy.io import loadmat


# Get Data
eeg_data_path = "data/EEG"
aud_data_path = "data/AUDIO"
eeg_files = os.listdir(eeg_data_path)
eeg_files = natsorted(eeg_files)
audio_files = os.listdir(aud_data_path)

n_channels = 64
target_sr = 64


def load_subject(subject_path):
    mat_subject = loadmat(subject_path)
    data = mat["data"]
    info = mat["expinfo"]

     # EEG Variables
    eeg_sr = data["fsample"].item()["eeg"].item()[0][0]
    events = data["event"].item()["eeg"].item()["sample"].item()
    events = events.flatten()


    # Go through every trial of this subject
    n_trials = len(events) // 2
    trials = []

    for trial_idx in range(n_trials):
        trial = load_trial(data, info, trial_idx, events, eeg_sr)
        if trial is not None:
            trials.append()
    
    del data, info
    return trials



def load_trial(data, info, trial_idx, events, eeg_sr):

    # Skip Single-Speaker Trials
    male_field = info["wavfile_male"][trial_idx][0]
    female_field = info["wavfile_female"][trial_idx][0]

    if len(female_field) == 0 or len(male_field) == 0:
        return None
    
    # Extract EEG sample for this trial
    start_sample = events[2 * trial_idx]
    end_sample = events[2 * trial_idx + 1]
    eeg = data["eeg"].item()[0, 0][start_sample:end_sample, :n_channels].T

    # Extract label
    label_raw = info["attend_mf"][trial_idx]
    label = int(label_raw[0][0][0]) - 1

    # Extract stimulus files
    stimuli = [male_field[0], female_field[0]]

    # Load audio
    audio = []
    audio_sr = []
    for stim_file in stimuli:
        stim_path = audio_dir / stim_file
        sr, wav = read_wav(stim_path)
        audio.append(wav)
        audio_sr.append(sr)
    
    eeg, audio = preproc(eeg, audio, eeg_sr, audio_sr, target_sr)
    
    return {"eeg": eeg, "audio": audio, "label": label, "stimuli": stimuli}


def load_dataset():
    subject_files = [file for file in os.listdir(eeg_data_path)]
    subject_files = natsorted(subject_files)
    dataset = []

    for subject_idx in len(subject_files):
        subject_path = os.path.join(eeg_data_path, eeg_files[subject_idx])
        trials = load_subject(subject_path, audio_dir)
        dataset.append(trials)
        del trials
    
    return dataset



s_data_list = load_dataset()
np.save("s_data_list", s_data_list)
