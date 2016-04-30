from numpy import array
import librosa
from sklearn.preprocessing import MinMaxScaler
import numpy as np

features = [
    "zero_crossing_rate",
    "spectral_centroid",
    "spectral_bandwidth",
    "spectral_contrast",
    "spectral_rolloff",
    "rmse",
    #"tonnetz",         # taking lot of time to compute
    "mfcc"
]

def extract_features(signal, features):
    fvs = list()
    for feature_name in features:
        if feature_name == 'zero_crossing_rate':
            fvs.extend(librosa.feature.zero_crossing_rate(signal))
        elif feature_name == 'spectral_centroid':
            fvs.extend(librosa.feature.spectral_centroid(signal))
        elif feature_name == 'spectral_bandwidth':
            fvs.extend(librosa.feature.spectral_bandwidth(signal))
        elif feature_name == 'spectral_contrast':
            fvs.extend(librosa.feature.spectral_contrast(signal))
        elif feature_name == 'spectral_rolloff':
            fvs.extend(librosa.feature.spectral_rolloff(signal))
        elif feature_name == 'rmse':
            fvs.extend(librosa.feature.rmse(signal))
        elif feature_name == 'tonnetz':
            fvs.extend(librosa.feature.tonnetz(signal))
        elif feature_name == 'mfcc':
            n_mfcc = 7
            mfccs = librosa.feature.mfcc(signal)
            fvs.extend(mfccs[:n_mfcc,:])

    return fvs

def createVector(filename):
    """ Create a feature vector from audio file """
    signal, fs = librosa.load(filename)

    song_features = np.array(extract_features(signal, features))

    mean = song_features.mean(axis=1)
    covar = np.cov(song_features, rowvar=1)

    iu1= np.triu_indices(covar.shape[0])
    ravelcovar = covar[iu1]
    
    mean.resize(1,mean.shape[0])

    return np.append(mean, ravelcovar)