import librosa
from MusicReco.models.db import *


a = Audio.select().get()
signal, fs = librosa.load(a.path)

f1 = librosa.feature.zero_crossing_rate(signal)
f2 = librosa.feature.spectral_centroid(signal)
f3 = librosa.feature.mfcc(signal, sr=fs)
f4 = librosa.feature.spectral_bandwidth(signal)
f5 = librosa.feature.spectral_contrast(signal)
f6 = librosa.feature.chroma_stft(signal)
print(f1.shape)
print(f2.shape)
print(f3.shape)
print(f4.shape)
print(f5.shape)
print(f6.shape)

