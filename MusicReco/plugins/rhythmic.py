import numpy as np
import librosa

def createVector(filename):
    """ Create a feature vector from audio file """
    # It is a jewel in feature extraction which captures chromagram along with MFCC features
    # It has to be good for audio genre classification
    signal, sr = librosa.load(filename)
    y_harmonic, y_percussive = librosa.effects.hpss(signal)
    n_mfcc = 5
    tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,
                                                 sr=sr)
    mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=n_mfcc)
    
    mfcc_delta = librosa.feature.delta(mfcc)

    #beat_mfcc_delta = librosa.feature.sync(np.vstack([mfcc, mfcc_delta]),
    #                                       beat_frames)

    chromagram = librosa.feature.chroma_stft(y=signal,
                                            sr=sr, n_chroma=12)

    #beat_chroma = librosa.feature.sync(chromagram,
    #                                   beat_frames,aggregate=np.median)

    beat_features = np.vstack([chromagram, mfcc_delta])

   
    mean = beat_features.mean(axis=1)
    covar = np.cov(beat_features, rowvar =1)
    
    iu1= np.triu_indices(mean.shape[0])
    ravelcovar = covar[iu1]
    
    mean.resize(1,mean.shape[0])

    return np.append(mean,ravelcovar)