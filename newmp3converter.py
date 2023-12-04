import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# Creating root window
root = tk.Tk()
root.title('Select Audio File.')
root.resizable(False, False)
root.geometry('300x150')

selected_file = ""


def select_file():
    filetypes = (
        ('WAV files', '*.wav'),
        ('MP3 files', '*.mp3'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a File',
        initialdir='/',
        filetypes=filetypes)

    # Holds the path of the selected file.
    selected_file = filename

    # tkinter.messagebox — Tkinter message prompts
    showinfo(
        title='Selected File',
        message=filename)

    print(selected_file)


# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)
open_button.pack(expand=True)

# run the application
root.mainloop()
# Holds all the possible files for testing and randomly selects a file for testing
files = selected_file   # "conver.mp3"

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
