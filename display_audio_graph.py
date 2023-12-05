import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment


def display_audio(path):

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
                label_title = f'Channel {x + 1}'
                plt.plot(time, data[:, x], label=label_title)

    # Holds all the possible files for testing and randomly selects a file for testing
    source = path    # when this is a straight string it works but with tkinter gui it breaks

    # File used to store converted mp3
    destination = "test.wav"

    wav_filename = ""
    # Determines if the file is not a wav and does a mp3 to wav conversion
    # Then associates wav_filename with appropriate filename

    if source.find(".mp3") != -1:
        sound = AudioSegment.from_mp3(source)
        sound.export(destination, format="wav")
        wav_filename = destination
    elif source.find(".wav") != -1:
        wav_filename = source
    else:
        print("Gah")
    samplerate, data = wavfile.read(wav_filename)
    length = data.shape[0] / samplerate

    # 1chan: 101430, 44100, 2.3s
    # 2chan: 2, 44100, 0.4658s
    # 4chan: 4, 44100, 2.3s

    time = np.linspace(0, length, data.shape[0])
    plot_labeling(define_channel_count())
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()
