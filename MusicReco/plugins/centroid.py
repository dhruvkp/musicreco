from numpy import array
import librosa
#import sklearn.preprocessing.MinMaxScaler

def extract_features(signal, features):
    fvs = list()
    for feature_name in features:
        if feature_name == 'zero_crossing_rate':
            fvs.append(librosa.feature.zero_crossing_rate(signal)[0, 0])
        elif feature_name == 'spectral_centroid':
            fvs.append(librosa.feature.spectral_centroid(signal)[0, 0])
    return fvs

def createVector(filename):
    """ Create a feature vector from audio file """
    signal, fs = librosa.load(filename)
    features = ('zero_crossing_rate', 'spectral_centroid')

    song_features = array([extract_features(signal, features)])
    return song_features
