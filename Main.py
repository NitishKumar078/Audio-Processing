import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkhtmlview import HTMLLabel

import subprocess
import threading
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
            if os.path.isfile('./.audio.wav'):
                os.remove(".audio.wav")
            if os.path.isfile('./.transcription.txt'):
                os.remove(".transcription.txt")
            # list_desktop_files()
        except FileNotFoundError as e:
            print("Somthing went wrong : ",e )
    root.destroy()

def select_file():
    filetypes = (('Video files', '*.mp4'),)
    selected_filename = fd.askopenfilename(
        title='Select a file',
        initialdir='./',
        filetypes=filetypes)
    if selected_filename:
        file_path.set(selected_filename)  # Update the selected file path

# Function to perform an operation on the selected file
def process_file():
    selected_file = file_path.get()
    if selected_file:
        # Call the processing functions in a separate thread
        threading.Thread(target=process_audio, args=(selected_file,)).start()
        threading.Thread(target=process_transcription).start()
        DA_button.config(state="normal")
        DT_button.config(state="normal")
    else:
       messagebox.showwarning("Error", "Please select a file properly.")

def process_audio(selected_file):
    command = f'ffmpeg -i "{selected_file}" -ab 160k -ar 44100 -vn .audio.wav'
    subprocess.call(command, shell=True)
    win32file.SetFileAttributes(".audio.wav", win32con.FILE_ATTRIBUTE_HIDDEN)
    print("Audio processing completed.")

def process_transcription():
    model = whisper.load_model("base") 
    result = model.transcribe("./.audio.wav")
    with open(".transcription.txt", "w", encoding="utf-8") as f:
        lines = result["text"].replace(',', '\n')
        clear_text(text_widget)
        add_text(text_widget, lines)
        f.write(lines)
    win32file.SetFileAttributes(".transcription.txt", win32con.FILE_ATTRIBUTE_HIDDEN)
    print("Transcription processing completed.")



def add_text(text_widget, text):
    text_widget.insert('end', text)

def clear_text(text_widget):
    text_widget.delete('1.0', 'end')

def texttospeech(text_widget):
    global text_speech  # Declare text_speech as a global variable to stop the speech later 
        # Initialize the text-to-speech engine
    text_speech = pyttsx3.init()
    text_speech.setProperty('rate', 180) 
    rate = text_speech.getProperty('rate')
    text_speech.say("speech rate is " + str(rate))

    # Replace commas with newlines
    text = text_widget.get('1.0', 'end-1c')  # Get the text from line 1, column 0 to the end minus one character (i.e., exclude the newline character)
    # print(text)
    line = text
    text_speech.say(line)
    text_speech.runAndWait() 

def stop_speech():
    text_speech.stop()

def DAudio():
    # Remove the hidden attribute from the file
    if messagebox.askokcancel("Download", " Do you want to download ?"):
            win32file.SetFileAttributes(".audio.wav", win32con.FILE_ATTRIBUTE_NORMAL)
            os.rename('.audio.wav', 'audio.wav')
            
def DTxt(text_widget):
    # Remove the hidden attribute from the file
    text = text_widget.get('1.0', 'end-1c')
    win32file.SetFileAttributes(".transcription.txt", win32con.FILE_ATTRIBUTE_NORMAL)
    os.rename('.transcription.txt', 'transcription.txt')
    if messagebox.askokcancel("Update", " Do you want to update the text file ?"):
        with open("transcription.txt", "w", encoding="utf-8") as f:
            f.write(text) 

def add_text(text_widget, text):
    # Use the insert method to add text at the end of the Text widget
    text_widget.insert('end', text)

# Create the root window
root = tk.Tk()
root.title('File Processing Tool')
root.resizable(True,True)
root.geometry("760x600")
# Create a ttk style
style = ttk.Style()

# Set the theme to use
style.theme_use("clam")  # Any theme name you want to use

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


speech_button = ttk.Button(root, text='Text to Speech', command=lambda: threading.Thread(target=texttospeech,args=(text_widget,)).start())
speech_button.grid(row=2, column=6, columnspan=2,padx=5, pady=5, sticky='we')

# Create a button to pause speech
pause_button = ttk.Button(root, text="Pause Speech", command=stop_speech)
pause_button.grid(row=3, column=6, columnspan=2, padx=5, pady=5, sticky='we')


# Create a Text widget
text_widget = tk.Text(root, wrap='word') 
text_widget.grid(row=2, column=0,columnspan=4,rowspan=4, padx=5, pady=5,sticky="nsew")
add_text(text_widget, 'its just text area')


# Button to DOWNLOAD
DA_button = ttk.Button(root, text='DOWNLOAD AUDIO' ,command=DAudio , state="disabled" )
DA_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='we')
DT_button = ttk.Button(root, text='DOWNLOAD TEXT',command=lambda: threading.Thread(target=DTxt,args=(text_widget,)).start(), state="disabled" )
DT_button.grid(row=6, column=2, columnspan=2, padx=5, pady=5, sticky='we')




root.protocol("WM_DELETE_WINDOW", on_closing)  # Bind on_closing function to window close event

# Run the application
root.mainloop()