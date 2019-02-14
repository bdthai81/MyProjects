import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

fs=44100
duration = 2  # seconds

myrecording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float64')
print("Recording Audio")
sd.wait()
myrecording2 = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float64')
sd.wait()
print("Audio recording complete, Play Audio")
sd.play(myrecording, fs)
sd.wait()
sd.play(myrecording2, fs)
sd.wait()
print("Play Audio Complete")