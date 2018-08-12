# -*- coding:utf-8 -*-
import pyaudio
import wave
import numpy as np
from tkinter import *
import sys
import threading


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.button_start = Button(self, text="START", command=self.press_button_start)
        self.button_start.grid()
        self.button_stop = Button(self, text="STOP", command=self.press_button_stop)
        self.button_stop.grid()

    def press_button_start():
        global is_streaming
        global my_thread
    
        if not is_streaming:
            is_streaming = True
            my_thread = threading.Thread(target=self.stream_start)
            my_thread.start()
    
    def press_button_stop():
        global is_streaming
        global my_thread
    
        if is_streaming:
            is_streaming = False
            my_thread.join()
            
    def stream_start():
        CHUNK = 2048
        RATE = 44100
        threshold = 0.01
        global is_streaming
        p=pyaudio.PyAudio()
        wf = wave.open('gorilla_cry.wav', 'rb')
        #wff = wf.readframes(wf.getnframes())
        wff = wf.readframes(CHUNK)
        stream=p.open(
                format = pyaudio.paInt16,
        	    channels = 1,
        		rate = RATE,
        		frames_per_buffer = CHUNK,
        		input = True,
        		output = True) # inputとoutputを同時にTrueにする
        
        
        def audio_trans(input):
            x = np.frombuffer(input, dtype="int16") / 32768.0
            if x.max() > threshold:
                return wff
            else:
                return ''
        
        while stream.is_active() and is_streaming:
            input = stream.read(CHUNK,  exception_on_overflow = False)
            input = audio_trans(input)
            output = stream.write(input)
            
        stream.stop_stream()
        stream.close()
        p.terminate() 
    
is_streaming = False
my_thread = None

root = Tk()
root.title("GVC")
root.geometry("400x300")
app = Application(master=root)
app.mainloop()
