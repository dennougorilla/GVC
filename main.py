# -*- coding:utf-8 -*-
import pyaudio
import wave
import numpy as np
from tkinter import *
import tkinter.ttk as ttk
import sys
import threading
import os


def resource_path(relative): 
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

def get_device_list():
    p = pyaudio.PyAudio()
    #device info type is dict
    device_li = [p.get_device_info_by_index(i) for i in range(p.get_device_count())]
    return device_li

def stream_start():
    CHUNK = 2048
    RATE = 44100
    threshold = 0.01
    global is_streaming
    global INPUT
    global OUTPUT
    p=pyaudio.PyAudio()
    wf = wave.open(resource_path('./gorilla_cry.wav'), 'rb')
    #wff = wf.readframes(wf.getnframes())
    wff = wf.readframes(CHUNK)
    stream=p.open(
            format = pyaudio.paInt16,
    	    channels = 1,
    		rate = RATE,
    		frames_per_buffer = CHUNK,
                input_device_index = INPUT,
                output_device_index = OUTPUT,
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

def run_statusbar():
    status.configure(text="Now processing.." + 'input=' + str(INPUT) + ' ' + 'output=' + str(OUTPUT))

def kill_statusbar():
    status.configure(text="")

def press_button_start():
    global is_streaming
    global my_thread

    global INPUT 
    global OUTPUT

    INPUT = int(input_combo.get()[1])
    OUTPUT = int(output_combo.get()[1])

    if not is_streaming:
        is_streaming = True
        run_statusbar()
        my_thread = threading.Thread(target=stream_start)
        my_thread.start()

def press_button_stop():
    global is_streaming
    global my_thread

    if is_streaming:
        is_streaming = False
        my_thread.join()
        kill_statusbar()
        
is_streaming = False
my_thread = None
INPUT = ''
OUTPUT = ''

device_li = get_device_list()

root = Tk()
root.title("GVC")
root.geometry("400x300")

input_combo = ttk.Combobox(root, state='readonly')
input_combo["values"] = tuple('['+str(i)+']'+' '+device_li[i]['name'] for i in range(len(device_li)))
input_combo.current(0)
input_combo.pack()

output_combo = ttk.Combobox(root, state='readonly')
output_combo["values"] = tuple('['+str(i)+']'+' '+device_li[i]['name'] for i in range(len(device_li)))
output_combo.current(1)
output_combo.pack()


status = Label(root, text="", borderwidth=2, relief="groove")
status.pack(side=BOTTOM, fill=X)
button_start = Button(root, text="START", command=press_button_start)
button_start.pack()
button_stop = Button(root, text="STOP", command=press_button_stop)
button_stop.pack()

root.mainloop()
