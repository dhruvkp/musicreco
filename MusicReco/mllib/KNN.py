from .base import Base
from MusicReco.models.db import *
import numpy as np
from collections import OrderedDict, Counter
from operator import itemgetter

gamma = 0.068

def kl_divergence(sigma1, sigma2, mu1, mu2):
    sigma2_inv = np.linalg.inv(sigma2)
    mean_diff = (mu1 - mu2)

    return np.log(np.linalg.det(sigma1)/np.linalg.det(sigma2)) 
    + np.trace(sigma2_inv.dot(sigma1)) - mu1.shape[0] 
    + mean_diff.T.dot(sigma2_inv).dot(mean_diff)

def KLsymmetric(sigma1, sigma2, mu1, mu2):
	sigma1_inv = np.linalg.inv(sigma1)
	sigma2_inv = np.linalg.inv(sigma2)
	mean_diff = mu1 - mu2
	kl = np.trace(sigma2_inv.dot(sigma1) + sigma1_inv.dot(sigma2)) - 2*mu1.shape[0] + mean_diff.T.dot(sigma2_inv + sigma1_inv).dot(mean_diff)

	return np.exp(-gamma* kl)
	#return np.abs(0.5*(kl_divergence(sigma1, sigma2, mu1, mu2) + kl_divergence(sigma2, sigma1, mu2, mu1)))


class KNN(Base):
	""" K Nearest neighbours for Music classification 
		
		It requires guassian mixture model to work with which requires mean and covariance matrices. Hence it is compatible with 
		currently mfcc_simple.py
	"""

	def __init__(self, k=5):
		super(KNN, self).__init__()
		self.k = k

	def train(self, data=None, plugin=None):
		""" Training through KNN """
		super(KNN, self).train(data, plugin)
		# It contains 1 X N mean vectors and N X N covariance matrix where N is
		# spectral features in MFCC.

		#print(X[0].shape)
		
		# no training required .. YIPEE !
		

	def predict(self,file, plugin = None):
		""" GUESS the output of single file """
		super(KNN, self).predict(file, plugin)
		data = file.vector[plugin]
		rows = {}

		# go through all the files and pick all training samples where GMM plugin Output generated
		files = Audio.select().filter(state=1).filter(istest=0)
		for file in files:
			gmm = file.vector[plugin]
			rows[(file.name, file.genre)] = KLsymmetric(gmm[1:,:], data[1:,:], gmm[0,:],data[0,:])
		
		sorted_rows = sorted(rows.items(), key= lambda x: x[1])[:self.k]

		cnt = Counter()
		
		#print("KNN : file", file.name)
		for key,value in sorted_rows:
			#print(key, value)
			cnt[key] += 1
			
		# find the max count class
		return max(cnt)[1]