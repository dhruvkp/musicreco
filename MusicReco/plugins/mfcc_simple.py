import numpy as np
import librosa

def createVector(filename):
    """ Create a feature vector from audio file """
    # it captures complete MFCC features 20. It is very much similar to GMM_plugin
    # May be redundant, Can be removed in future updates.

    # UPDATE: ignoring first 30% and last 30% frames to calculate mfcc feature vectors.
    
    signal, fs = librosa.load(filename)
    mfccs = librosa.feature.mfcc(signal, sr=fs)

    # Simple MFCC feature vectors FULL set
    
    l = mfccs.shape[1]
    mfccs = mfccs[:,int(0.1*l):int(0.9*l)]
    
    mean = mfccs.mean(axis=1)
    covar = np.cov(mfccs, rowvar =1)
    
    mean.resize(1, mean.shape[0])
    # it returns matrix.. not useful for machine learning algorithms except KNN
    return np.concatenate((mean, covar) ,axis=0)