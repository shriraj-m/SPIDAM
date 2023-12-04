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



'''
spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
# select a frequency under 1kHz
def find_target_frequency(freqs):
    for x in freqs:
        if x > 1000:
            break
        return x


def frequency_check():
    # identify a frequency to check
    global target_frequency
    target_frequency = find_target_frequency(freqs)
    index_of_frequency = np.where(freqs == target_frequency)[0][0]
    # find sound data for a particular frequency
    data_for_frequency = spectrum[index_of_frequency]
    # change a digital signal for a values in decibels
    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun


data_in_db = frequency_check()
plt.figure(2)
plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color="#004bc6")
plt.xlabel("Time (s)")
plt.ylabel("Power (dB)")

# find a index of a max value
index_of_max = np.argmax(data_in_db)
value_of_max = data_in_db[index_of_max]
plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')

# slice our array from a max value
sliced_array = data_in_db[index_of_max:]
value_of_max_less_5 = value_of_max - 5


# find nearest value of less 5db
def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

# slice array from a max -5db
value_of_max_less_25 = value_of_max - 25
value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
print(f'rt20= {rt20}')
rt60 = 3*rt20
#plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))
plt.grid()
plt.show()
print(f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')

'''

