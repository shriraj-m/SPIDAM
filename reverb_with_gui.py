import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from display_audio_graph import display_audio
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from reverb import reverb_implementation

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
        ('All Files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a File',
        initialdir='/',
        filetypes=filetypes)

    # Holds the path of the selected file.
    selected_file = filename

    # tkinter.messagebox — Tkinter message prompts


    #print(f'#1 {selected_file}')
    if selected_file.find(".wav") == -1 and selected_file.find(".mp3") == -1:
        messagebox.showerror("Invalid File Type", "Error: The file type selected is not supported")
    else:
        display_audio(selected_file)
        sample_rate, data = wavfile.read(selected_file)
        if len(data.shape) == 1:
            spectrum, freq, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
            reverb_implementation(spectrum, freq, t)

        else:
            channel_count = data.shape[1]
            for x in range(channel_count):
                spectrum, freq, t, im = plt.specgram(data[:, x], Fs=sample_rate, NFFT=1024,
                                                     cmap=plt.get_cmap('autumn_r'))
                reverb_implementation(spectrum, freq, t)

# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)
open_button.pack(expand=True)
exit_button = ttk.Button(
    root,
    text="EXIT",
    command=root.destroy
)
exit_button.pack()

# run the application
root.mainloop()

