
import tkinter as tk
import numpy as np
import wave
import sys
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.io


wav_filename = ("16bit4chan.wav")
samplerate, data = wavfile.read(wav_filename)
print(data.shape[len(data.shape) - 1])
print(samplerate)
length = data.shape[0] / samplerate
print(length)

# 1chan: 101430, 44100, 2.3s
# 2chan: 2, 44100, 0.4658s
# 4chan: 4, 44100, 2.3s

time = np.linspace(0, length, data.shape[0])
print(time)
plt.plot(time, data, label="First Channel")
'''
plt.plot(time, data[:, 1], label="Second Channel")  
plt.plot(time, data[:, 2], label="Third channel")
plt.plot(time, data[:, 3], label="Fourth Channel")'''
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()


'''
import tkinter as tk
import numpy as np
import wave
import sys
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.io


wav_filename = ("16bit4chan.wav")
samplerate, data = wavfile.read(wav_filename)
print(data.shape[len(data.shape) - 1])
print(samplerate)
length = data.shape[0] / samplerate
print(length)

# 1chan: 101430, 44100, 2.3s
# 2chan: 2, 44100, 0.4658s
# 4chan: 4, 44100, 2.3s

time = np.linspace(0, length, data.shape[0])
print(time)
plt.plot(time, data, label="Left channel")
# plt.plot(time, data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
'''