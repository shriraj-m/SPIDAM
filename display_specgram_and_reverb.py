# ReverbTime 0
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from find_frequency import find_target_frequency
from reverb import reverb_implementation

sample_rate, data = wavfile.read("16bit4chan.wav")
if len(data.shape) == 1:
    spectrum, freq, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    reverb_implementation(spectrum, freq, t)

else:
    channel_count = data.shape[1]
    for x in range(channel_count):
        spectrum, freq, t, im = plt.specgram(data[:, x], Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        reverb_implementation(spectrum, freq, t)
