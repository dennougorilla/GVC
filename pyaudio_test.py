# -*- coding:utf-8 -*-
import pyaudio
import wave
import numpy as np

def stream():
    CHUNK=1024*2
    RATE=44100
    threshold = 0.01
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
    
    while stream.is_active():
        input = stream.read(CHUNK)
        input = audio_trans(input)
        output = stream.write(input)
        
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    print("Stop Streaming")
