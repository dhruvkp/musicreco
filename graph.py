from MusicReco.models.db import *
from config import settings
import librosa

import matplotlib.pyplot as plt
import numpy as np

#plt.colorbar(format='%+2.0f dB')

# f, axarr = plt.subplots(5, 2)

for cnt,tag in enumerate(settings['tags']):
  a = Audio.select().join(Tag).where(Tag.genre==tag).get()

  print(a.name)
  #y, sr=librosa.load(a.path)
  y, sr =librosa.load(settings['training_dataset']+'/'+tag+'/'+a.name)
  #S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
  #librosa.display.specshow(librosa.logamplitude(S, ref_power= np.max), y_axis = 'mel', fmax=8000, x_axis='time')
  # mfccs = librosa.feature.chroma_stft(y=y, sr=sr, n_chroma=8)
  mfccs = librosa.feature.zero_crossing_rate(y=y)
  plt.subplot(5,2,cnt+1)
  librosa.display.specshow(mfccs, x_axis='time', y_axis='mel')
  plt.title("ZCR "+tag)
plt.tight_layout()
fname = "ZCR_fig.png"
plt.savefig(fname)
