import numpy as np
import librosa

def createVector(filename):
	""" Create a feature vector from filename"""
	signal, fs = librosa.load(filename)
    mfccs = librosa.feature.mfcc(signal, sr=fs)

   	mean = mfccs.mean(axis=1)
   	covar = np.cov(mfccs, rowvar=1)

   	