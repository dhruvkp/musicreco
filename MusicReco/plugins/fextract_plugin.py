from numpy import array
import librosa

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
    mfccs = librosa.feature.mfcc(signal, sr=fs)

    # MFCCS are two dimensional data. Need to save it
    # Either we can use Dynamic Time Warping to calculate distance
    # between two songs

    # MFCC is of 20 feature vector for each frame ( 300 frames approx. )
    # Either we represent them using gaussian distribution mu, Sigma
    # or we take some average

    # With guassian, we can approximate difference between two probabilties ( KL divergence, can use variational inference VERY IMPORTANT )


    return mfccs
