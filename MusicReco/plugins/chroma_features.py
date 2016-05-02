import numpy as np
import librosa

def createVector(filename):
	""" Create a feature vector from filename"""
	# This captures 12 mfcc features along with its covariance 

	# UPDATE: ignoring first 30% and last 30% frames to calculate mfcc feature vectors.
	# UPDATE: Testing it for chroma features.
	signal, fs = librosa.load(filename)
	n_mfcc = 12

	mfccs = librosa.feature.chroma_stft(signal, sr=fs, n_chroma=n_mfcc)

	l = mfccs.shape[1]
	mfccs = mfccs[:,int(0.1*l):int(0.9*l)]
	mean = mfccs.mean(axis=1)
	covar = np.cov(mfccs, rowvar=1)

	iu1= np.triu_indices(n_mfcc)
	ravelcovar = covar[iu1]
	
	mean.resize(1,n_mfcc)

	return np.append(mean,ravelcovar)