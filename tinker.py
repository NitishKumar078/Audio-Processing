# IMPORT for thinker for UI

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# IMPORT for Conversion of Videofile into audio
# import subprocess
# import whisper
# from ibm_watson import SpeechToTextV1
# from ibm_watson.websocket import RecognizeCallback, AudioSource
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator





# Create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')

# Variable to store the selected file ...  
SelectedFile = None 

def select_file():
    filetypes = (
        ('All files', '.'),
        ('video file', '*.mp4')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    # making SelectedFile as global 
    global  SelectedFile
    # Assig the file path ...
    SelectedFile = filename
   
def fun(SelectedFile):
    print("insted the fun ", SelectedFile)
    command = f'ffmpeg -i {SelectedFile} -ab 160k -ar 44100 -vn audio.wav'
    subprocess.call(command, shell=True)

    # result = model.transcribe("venv/files/test1.mp3", fp16=False)

    model = whisper.load_model("base")
    result = model.transcribe("./audio.wav")

    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(result["text"])

# Button intiallazation ...
open_button = ttk.Button(root,text='Open a File',command=select_file)

open_button.pack(expand=True)






printt = ttk.Button(root,text="print",command=fun)
printt.pack(expand=True)

# run the application on loop 
root.mainloop()