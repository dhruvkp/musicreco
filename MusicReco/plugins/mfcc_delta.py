import numpy as np
import librosa

def createVector(filename):
    """ Create a feature vector from audio file """

    # MFCC features extraction along with delta.
    
    # Delta captures change in values from one one frame to another, important to capture
    # transaction features for classification
    # UPDATE: ignoring first 30% and last 30% frames to calculate mfcc feature vectors.
    
    signal, fs = librosa.load(filename)
    n_mfcc = 7
    mfccs = librosa.feature.mfcc(signal, sr=fs, n_mfcc=n_mfcc)

    
    delta = librosa.feature.delta(mfccs)
    
    mfccs = np.concatenate( (mfccs,delta) ,axis=0)

    l = mfccs.shape[1]
    mfccs = mfccs[:,int(0.1*l):int(0.9*l)]
    
    mean = mfccs.mean(axis=1)
    covar = np.cov(mfccs, rowvar =1)
    
    iu1= np.triu_indices(mean.shape[0])
    ravelcovar = covar[iu1]
    
    mean.resize(1,mean.shape[0])

    return np.append(mean,ravelcovar)