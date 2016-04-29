import numpy as np
import librosa

def createVector(filename):
	""" Create a feature vector from filename"""
	signal, fs = librosa.load(filename)
	n_mfcc = 12

	mfccs = librosa.feature.mfcc(signal, sr=fs, n_mfcc=n_mfcc)
	
	mean = mfccs.mean(axis=1)
	covar = np.cov(mfccs, rowvar=1)

	mean.resize(1,n_mfcc)
	return np.concatenate((mean, covar), axis=0)