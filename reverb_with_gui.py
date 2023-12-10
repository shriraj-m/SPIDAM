import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from pydub import AudioSegment
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from find_frequency import find_target_frequency
from scipy.signal import welch

# Creating root window
root = tk.Tk()
root.title('Select Audio File.')
root.config(bg="skyblue")
root.resizable(True, True)
root.geometry('1280x720')

header = tk.Frame(root)
header.grid(row=0, column=1, padx=10, pady=10)

center_top = tk.Frame(root)
center_top.grid(row=1, padx=10, pady=10)

center_bot = tk.Frame(root)
center_bot.grid(row=2, padx=10, pady=10)

footer = tk.Frame(root)
footer.grid(row=3, column=1, padx=10, pady=10)

selected_file = ""


def display_audio(path):
    ax1.clear()

    def define_channel_count():
        if len(data.shape) == 1:
            return 1
        else:
            return data.shape[1]

    def plot_labeling(channel_count):
        if channel_count == 1:
            ax1.set_title("Audio Wavegraph")
            ax1.set_xlabel("Time [s]")
            ax1.set_ylabel("Amplitude")
            ax1.plot(time, data, label="Channel 1")
            ax1.legend()

        elif channel_count > 1:
            for x in range(channel_count):
                label_title = f'Channel {x + 1}'
                ax1.set_ylabel("Time [s]")
                ax1.set_ylabel("Amplitude")
                ax1.set_title("Audio Wavegraph")
                ax1.plot(time, data[:, x], label=label_title)
                ax1.legend()

    # Holds all the possible files for testing and randomly selects a file for testing
    source = path  # when this is a straight string it works but with tkinter gui it breaks

    # File used to store converted mp3
    destination = "test.wav"

    wav_filename = ""
    # Determines if the file is not a wav and does a mp3 to wav conversion
    # Then associates wav_filename with appropriate filename

    if source.find(".mp3") != -1:
        sound = AudioSegment.from_mp3(source)
        sound.export(destination, format="wav")
        wav_filename = destination
    elif source.find(".wav") or source.find(".WAV") != -1:
        wav_filename = source
    else:
        print("uhoh")
    samplerate, data = wavfile.read(wav_filename)
    if define_channel_count() == 1:
        frequencies, power = welch(data, samplerate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        reso_value = f'Resonance of Selected Graph: {round(dominant_frequency)}Hz.'
        resonance.config(text=reso_value)
    elif define_channel_count() > 1:
        # Only prioritize channel 1
        frequencies, power = welch(data[:, 0], samplerate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        reso_value = f'Resonance of Selected Graph: {round(dominant_frequency)}Hz.'
        resonance.config(text=reso_value)

    length = data.shape[0] / samplerate
    time_of_file = f'Time (in Seconds) of Selected File: {round(length, 2)}s.'
    time_value.config(text=time_of_file)

    time = np.linspace(0, length, data.shape[0])
    plot_labeling(define_channel_count())
    canvas1.draw()


def select_file():
    filetypes = (
        ('WAV files', '*.wav'),
        ('WAV files', '*.WAV'),
        ('MP3 files', '*.mp3'),
        ('All Files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a File',
        initialdir='/',
        filetypes=filetypes)

    # Holds the path of the selected file.
    global selected_file
    selected_file = filename
    print(selected_file)
    file_name.config(text=selected_file)

    if selected_file.find(".wav") == -1 and selected_file.find(".mp3") == -1 and selected_file.find(".WAV") == -1:
        messagebox.showerror("Invalid File Type", "Error: The file type selected is not supported")
    else:
        display_audio(selected_file)
        run(selected_file)


colors = ["c", "m", "b", "r"]


def run(given_file):
    ax2.clear()
    ax3.clear()
    sample_rate, data = wavfile.read(given_file)
    if len(data.shape) == 1:
        ax3.set_title("Spectrogram")
        spectrum, freq, t, im = ax3.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        canvas3.draw()
        reverb_implementation(spectrum, freq, t, colors[1], label_value=1)
        canvas2.draw()

    else:
        channel_count = data.shape[1]
        for x in range(channel_count):
            ax3.set_title("Spectrogram")
            spectrum, freq, t, im = ax3.specgram(data[:, x], Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
            canvas3.draw()  # shows first spectrogram plot.
            label_string = f'Channel {x + 1}'
            reverb_implementation(spectrum, freq, t, colors[x], label_value=label_string)
        canvas2.draw()


def reverb_implementation(spectrum, freq, t, color, label_value):
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
    # reverb line
    ax2.set_title("Reverb Graph")
    ax2.plot(t, data_in_db, color=color, linewidth=1, alpha=0.7, label=label_value)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Power (dB)")
    ax2.legend()

    # find an index of a max value
    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db[index_of_max]
    ax2.plot(t[index_of_max], data_in_db[index_of_max], 'go')

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
    ax2.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

    # slice array from a max -5db
    value_of_max_less_25 = value_of_max - 25
    value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
    index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
    ax2.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

    rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
    print(f'rt20= {rt20}')
    rt60 = 3 * rt20
    print(f'The RT60 reverb time at freq {int(data_in_db[index_of_max])}Hz is {round(abs(rt60), 2)} seconds')


# open button
open_button = ttk.Button(
    header,

    text='Open a File',
    command=select_file
)
open_button.pack(pady=20)

file_name = tk.Label(
    header,
    text=selected_file,
    fg='black',
)
file_name.pack()

time_value = tk.Label(
    footer,
    text="",
    fg="black"
)
time_value.pack()

resonance = tk.Label(
    footer,
    text="",
    fg="black"
)
resonance.pack()

exit_button = ttk.Button(
    footer,
    text="EXIT",
    command=root.destroy
)
exit_button.pack()

# wavegraph section in gui
frame1 = tk.Frame(root)
figure1 = plt.figure(figsize=(4, 4))
ax1 = figure1.add_subplot(111)
canvas1 = FigureCanvasTkAgg(figure1, frame1)
canvas1.get_tk_widget().pack()
toolbar1 = NavigationToolbar2Tk(canvas1, frame1, pack_toolbar=False)
toolbar1.update()
toolbar1.pack(anchor="w", fill=tk.X)
frame1.grid(row=1, column=0, padx=5, pady=20)

# frequency section in gui
frame2 = tk.Frame(root)
figure2 = plt.figure(figsize=(4, 4))
ax2 = figure2.add_subplot(111)
canvas2 = FigureCanvasTkAgg(figure2, frame2)
canvas2.get_tk_widget().pack()
toolbar2 = NavigationToolbar2Tk(canvas2, frame2, pack_toolbar=False)
toolbar2.update()
toolbar2.pack(anchor="w", fill=tk.X)
frame2.grid(row=1, column=1, padx=5, pady=20)

# specgram section in gui
frame3 = tk.Frame(root)
figure3 = plt.figure(figsize=(4, 4), )
ax3 = figure3.add_subplot(111)
canvas3 = FigureCanvasTkAgg(figure3, frame3)
canvas3.get_tk_widget().pack()
toolbar3 = NavigationToolbar2Tk(canvas3, frame3, pack_toolbar=False)
toolbar3.update()
toolbar3.pack(anchor="w", fill=tk.X)
frame3.grid(row=1, column=2, padx=5, pady=20)

# run the application
root.mainloop()
