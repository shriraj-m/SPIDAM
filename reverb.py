from scipy.io import wavfile
from find_frequency import find_target_frequency
import numpy as np
import matplotlib.pyplot as plt

colors = ["c", "m", "b", "r"]


def run(file_path):
    sample_rate, data = wavfile.read(file_path)
    if len(data.shape) == 1:
        spectrum, freq, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        reverb_implementation(spectrum, freq, t, colors[1], label_value=1, channels=1)

    else:
        channel_count = data.shape[1]
        for x in range(channel_count):
            spectrogram = plt.figure()
            spec = spectrogram.add_subplot(111)
            spectrum, freq, t, im = spec.specgram(data[:, x], Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
            spectrogram.show()  # shows first spectrogram plot.
            label_string = f'Channel {x + 1}'
            reverb_implementation(spectrum, freq, t, colors[x], label_value=label_string, channels=channel_count)
        plt.show()



def reverb_implementation(spectrum, freq, t, color, label_value, channels):
    def frequency_check():
        # identify a frequency to check
        global target_frequency
        target_frequency = find_target_frequency(freq)
        index_of_frequency = np.where(freq == target_frequency)[0][0]  # find sound data for a particular frequency
        data_for_frequency = spectrum[index_of_frequency]
        # change a digital signal for a values in decibels
        data_in_db_fun = 10 * np.log10(data_for_frequency)
        return data_in_db_fun

    data_in_db = frequency_check()
    plt.figure(2)
    # reverb line
    plt.plot(t, data_in_db, color=color, linewidth=1, alpha=0.7, label=label_value)
    plt.xlabel("Time (s)")
    plt.ylabel("Power (dB)")
    plt.legend()

    # find an index of a max value
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
    rt60 = 3 * rt20
    print(f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')
    plt.grid()
