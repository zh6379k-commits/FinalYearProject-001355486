%% convert tables in Fuglsang dataset to struct and save.
clear; close all; clc;
IN_PATH = 'C:\Users\Student\Documents\MATLAB\EEG'; % path of eeg data
OUT_PATH = 'C:\Users\Student\Documents\MATLAB\EEG_New'; % path of output eeg data

subjects = setdiff(1:18,[]);

for ss = 1:length(subjects)
    fprintf('Processing subject: %s\n', num2str(subjects(ss)));
    
    %% Load data
    load(fullfile(IN_PATH,['S' num2str(subjects(ss)) '.mat']));
    expinfo = table2struct(expinfo);
    save(fullfile(OUT_PATH,['S' num2str(subjects(ss)) '.mat']),'data', 'expinfo');
end
