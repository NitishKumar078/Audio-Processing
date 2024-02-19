import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkhtmlview import HTMLLabel

import subprocess
import whisper
import pyttsx3

import win32file
import win32con
import os

def list_desktop_files():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    files_on_desktop = os.listdir(desktop_path)
    print(files_on_desktop)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        try:
            os.remove(".audio.wav")
            os.remove(".transcription.txt")
            # list_desktop_files()
        except FileNotFoundError:
            print("One or both files were not found.")
    root.destroy()

def select_file():
    filetypes = (('Video files', '*.mp4'),)
    selected_filename = fd.askopenfilename(
        title='Select a file',
        initialdir='/',
        filetypes=filetypes)
    if selected_filename:
        file_path.set(selected_filename)  # Update the selected file path

# Function to perform an operation on the selected file
def process_file():
    # Button to display the Text to Speech
    diplay_audioButton()        
    selected_file = file_path.get()
    if selected_file:
        command = f'ffmpeg -i "{selected_file}" -ab 160k -ar 44100 -vn .audio.wav'
        subprocess.call(command, shell=True)
        # Set the file attribute to hidden
        win32file.SetFileAttributes(".audio.wav", win32con.FILE_ATTRIBUTE_HIDDEN)
        model = whisper.load_model("base") 
        result = model.transcribe("./.audio.wav")
        with open(".transcription.txt", "w", encoding="utf-8") as f:
            lines=result["text"].replace(',', '\n')
            f.write(lines)
        print("Process completed successfully.")
        # Set the file attribute to hidden
        win32file.SetFileAttributes(".transcription.txt", win32con.FILE_ATTRIBUTE_HIDDEN)

# Function to stop the speech
def stop_speech():
    text_speech.stop()

def texttospeech():
    # Initialize the text-to-speech engine
    text_speech = pyttsx3.init()

    # Open the file and read lines
    with open('./.transcription.txt') as f:
        lines = f.readlines()
    
    # Replace commas with newlines
    lines = [line.replace(',', '\n') for line in lines]

    # Say each line and wait for it to complete before saying the next line
    for line in lines:
        text_speech.say(line)
        text_speech.runAndWait()


def diplay_audioButton():
    process_button = ttk.Button(root, text='Text to Speech', command=texttospeech)
    process_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='we')

    # Create a label to display text
    label = ttk.Label(root, text="Press the button to pause speech:")
    label.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='we')

    # Create a button to pause speech
    pause_button = ttk.Button(root, text="Pause Speech", command=texttospeech)
    pause_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='we')

def DAudio():
    # Remove the hidden attribute from the file
    win32file.SetFileAttributes("audio.wav", win32con.FILE_ATTRIBUTE_NORMAL)

def DTxt():
    # Remove the hidden attribute from the file
    win32file.SetFileAttributes("transcription.txt", win32con.FILE_ATTRIBUTE_NORMAL)


# Create the root window
root = tk.Tk()
root.title('File Processing Tool')
root.resizable(True,False)
root.geometry("700x300")

# Variable to store the selected file path
file_path = tk.StringVar()

# Label for file selection
file_label = ttk.Label(root, text='Selected File:')
file_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

# Entry widget to display the selected file path
file_entry = ttk.Label(root, textvariable=file_path, state='readonly')
file_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we' )

# Button to open file dialog
open_button = ttk.Button(root, text='Open File', command=select_file)
open_button.grid(row=0, column=2, padx=5, pady=5)

# Button to process the selected file
process_button = ttk.Button(root, text='Process File', command=process_file)
process_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='we')

process_button = ttk.Button(root, text='DOWNLOAD AUDIO' ,command=DAudio )
process_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='we')
process_button = ttk.Button(root, text='DOWNLOAD TEXT',command=DTxt )
process_button.grid(row=5, column=2, columnspan=2, padx=5, pady=5, sticky='we')

root.protocol("WM_DELETE_WINDOW", on_closing)  # Bind on_closing function to window close event

# Run the application
root.mainloop()
