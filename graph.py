from MusicReco.models.db import *
from config import settings
import librosa

import matplotlib.pyplot as plt
import numpy as np

#plt.colorbar(format='%+2.0f dB')

for tag in settings['tags']:
  a = Audio.select().join(Tag).where(Tag.genre==tag).get()

  print(a.name)
  fname = tag+"_fig.jpg"
  y, sr =librosa.load(a.path)
  #S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
  #librosa.display.specshow(librosa.logamplitude(S, ref_power= np.max), y_axis = 'mel', fmax=8000, x_axis='time')
  mfccs = librosa.feature.chroma_stft(y=y, sr=sr, n_chroma=8)
  librosa.display.specshow(mfccs, x_axis='time', y_axis='mel')
  plt.title("MFCC "+tag)
  plt.tight_layout()
  plt.savefig(fname)
