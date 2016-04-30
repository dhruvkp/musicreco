import numpy as np
import librosa

def createVector(filename):
    """ Create a feature vector from audio file """
    signal, fs = librosa.load(filename)
    mfccs = librosa.feature.mfcc(signal, sr=fs)

    # MFCCS are two dimensional data. Need to save it
    # Either we can use Dynamic Time Warping to calculate distance
    # between two songs

    # MFCC is of 20 feature vector for each frame ( 300 frames approx. )
    # Either we represent them using gaussian distribution mu, Sigma
    # or we take some average

    # With guassian, we can approximate difference between two probabilties ( KL divergence, can use variational inference VERY IMPORTANT )
    
    # mfccs are 20 X 1283 vectors
    # get covariance matrix
    mean = mfccs.mean(axis=1)
    covar = np.cov(mfccs, rowvar =1)

    mean.resize(1, mean.shape[0])
    return np.concatenate((mean, covar) ,axis=0)