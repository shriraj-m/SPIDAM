import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from display_audio_graph import display_audio

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

    print(f'#1 {selected_file}')
    display_audio(selected_file)

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

