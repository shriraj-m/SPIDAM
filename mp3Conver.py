import tkinter as tk
import numpy as np
import wave
import sys
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.io
from os import path
from pydub import AudioSegment



# Holds all the possible files for testing and randomly selects a file for testing
files = "C:/Users/smand/OneDrive/Desktop/GitThings/SPIDAM_project/16bit1chan.wav"   # "conver.mp3"

source = files
# File used to store converted mp3
destination = "test.wav"

wav_filename = ""
# Determines if the file is not a wav and does a mp3 to wav conversion
# Then associates wav_filename with appropriate filename
if source.find(".wav") == -1:
    sound = AudioSegment.from_mp3(source)
    sound.export(destination, format="wav")
    wav_filename = destination
else:
    wav_filename = source

samplerate, data = wavfile.read(wav_filename)
length = data.shape[0] / samplerate
time = np.linspace(0, length, data.shape[0])
# print(time)
plt.plot(time, data, label="First Channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
