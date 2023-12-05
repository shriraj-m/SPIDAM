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

'''selected_file = "C:/Users/smand/OneDrive/Desktop/GitThings/SPIDAM_project/16bit1chan.wav"
print(selected_file)
origin = selected_file
symbol = '/'
number = origin.find(symbol)
print(number)
source = selected_file[number:]
print(source)
'''