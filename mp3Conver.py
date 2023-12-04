
import tkinter as tk
import numpy as np
import wave
import sys
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.io
from os import path
from pydub import AudioSegment
import random
#

random.seed(None, 2)
#holds all the possible files for testing and randomly selects a file for testing
files = ["16bit1chan.wav", "16bit2chan.wav", "16bit4chan.wav", "conver.mp3"]
index = random.randint(0, files.__len__()-1)
source = files[index]
#file used to store converted mp3
destination = "test.wav"

wav_filename = ""

#determines if the file is not a wav and does a mp3 to wav conversion
#then associates wav_filename with appropriate filename
if(source.find(".wav")==-1):
    sound = AudioSegment.from_mp3(source)
    sound.export(destination, format="wav")
    wav_filename = destination
else:
    wav_filename = source

samplerate, data = wavfile.read(wav_filename)
#print(data.shape[len(data.shape) - 1])
#print(samplerate)
length = data.shape[0] / samplerate
#print(length)

# 1chan: 101430, 44100, 2.3s
# 2chan: 2, 44100, 0.4658s
# 4chan: 4, 44100, 2.3s

time = np.linspace(0, length, data.shape[0])
#print(time)
plt.plot(time, data, label="First Channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
