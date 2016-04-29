from .base import Base
from MusicReco.models.db import *
import numpy as np
from collections import OrderedDict, Counter
from operator import itemgetter

def kl_divergence(sigma1, sigma2, mu1, mu2):
    sigma2_inv = np.linalg.inv(sigma2)
    mean_diff = (mu1 - mu2)

    return np.log(np.linalg.det(sigma1)/np.linalg.det(sigma2)) 
    + np.trace(sigma2_inv.dot(sigma1)) - mu1.shape[0] 
    + mean_diff.T.dot(sigma2_inv).dot(mean_diff)

def KLsymmetric(sigma1, sigma2, mu1, mu2):
	return np.abs(kl_divergence(sigma2, sigma1, mu2, mu1))
	#return np.abs(0.5*(kl_divergence(sigma1, sigma2, mu1, mu2) + kl_divergence(sigma2, sigma1, mu2, mu1)))


class KNN(Base):
	def __init__(self, k=5):
		super(KNN, self).__init__()
		self.k = k

	def train(self, data=None):
		""" Training through KMeans """
		X = data['GMM']
		# It contains 1 X N mean vectors and N X N covariance matrix where N is
		# spectral features in MFCC.

		#print(X[0].shape)
		
		# no training required .. YIPEE !
		

	def predict(self,file):
		""" GUESS the output of single file """
		data = file.vector['GMM']
		rows = {}

		# go through all the files and pick all training samples where GMM plugin Output generated
		files = Audio.select().filter(state=1).filter(istest=0)
		for file in files:
			gmm = file.vector['GMM']
			rows[(file.name, file.genre)] = KLsymmetric(gmm[1:,:], data[1:,:], gmm[0,:],data[0,:])
		
		sorted_rows = sorted(rows.items(), key= lambda x: x[1])[:self.k]

		cnt = Counter()
		
		#print("KNN : file", file.name)
		for key,value in sorted_rows:
			#print(key, value)
			cnt[key] += 1
			
		# find the max count class
		return max(cnt)[1]