import librosa
from MusicReco.models.db import *
import numpy as np

a = Audio.get(id=40)
signal, fs = librosa.load(a.path)


#f1 = librosa.feature.zero_crossing_rate(signal)
#f2 = librosa.feature.spectral_centroid(signal)
#f3 = librosa.feature.mfcc(signal, sr=fs)
#f4 = librosa.feature.spectral_bandwidth(signal)
#f5 = librosa.feature.spectral_contrast(signal)
#f6 = librosa.feature.chroma_stft(signal)
#f7 = librosa.feature.delta(f3[:5,:])
#f8 = librosa.feature.tempogram(signal)
#temp, beats = librosa.beat.beat_track(signal)

y = signal
sr = fs

print("stage 0")
y_harmonic, y_percussive = librosa.effects.hpss(signal)

f1 = librosa.feature.chroma_cqt(y_harmonic,sr=sr)
print(f1.shape)
tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,
                                                 sr=sr)
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
print("stage 0.5")
mfcc_delta = librosa.feature.delta(mfcc)
print("stage 1")
beat_mfcc_delta = librosa.feature.sync(np.vstack([mfcc, mfcc_delta]),
                                           beat_frames)
print("stage 1.3")
chromagram = librosa.feature.chroma_stft(y=y_harmonic,
                                            sr=sr)
print("stage 1.5")
beat_chroma = librosa.feature.sync(chromagram,
                                       beat_frames,
                                                                          aggregate=np.median)
print("stage 2");
beat_features = np.vstack([beat_chroma, beat_mfcc_delta])
print(beat_features.shape)

