# import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


def define_channel_count():
    if len(data.shape) == 1:
        return 1
    else:
        return data.shape[1]


def plot_labeling(channel_count):
    if channel_count == 1:
        plt.plot(time, data, label="Channel 1")
    elif channel_count > 1:
        for x in range(channel_count):
            label_title = f'Channel {x+1}'
            plt.plot(time, data[:, x], label=label_title)


wav_filename = "16bit4chan.wav"
samplerate, data = wavfile.read(wav_filename)
length = data.shape[0] / samplerate

# 1chan: 101430, 44100, 2.3s
# 2chan: 2, 44100, 0.4658s
# 4chan: 4, 44100, 2.3s

time = np.linspace(0, length, data.shape[0])
plot_labeling(define_channel_count())
'''plt.plot(time, data[:, 1], label="Second Channel")
plt.plot(time, data[:, 2], label="Third channel")
plt.plot(time, data[:, 3], label="Fourth Channel")'''
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()

