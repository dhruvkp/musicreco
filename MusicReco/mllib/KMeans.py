from .base import Base
from sklearn.mixture import GMM
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA as sklearnPCA

class KMeans(Base):

	def __init__(self):
		super(KMeans, self).__init__()

	def train(self, data=None, plugin=None):
		""" Training through KMeans """
		super(KMeans, self).train(data, plugin)

		X = self.X_train.iloc[:,:-1]
		Y = self.X_train.iloc[:,-1]
		# It contains only N X M mfcc matrix
		n_classes = len(np.unique(self.X_train['class']))

		# create 10 clusters
		self.clf = GMM(n_components = n_classes, init_params='wc', n_iter=100, n_init=10, covariance_type='diag')

		# Initialize clf with each class mean
		#self.scaler = sklearnPCA(n_components=3).fit(X)
		self.scaler = StandardScaler().fit(X)
		X = self.scaler.transform(X)
		Y = Y.reshape(Y.shape[0],1)
		
		X = np.append(X, Y, 1)
		
		self.clf.means_ = np.array([ X[X[:,-1] == i][:,:-1].mean(axis=0) for i in range(n_classes)])
		
		self.clf.fit(X[:,:-1], Y)

	def predict(self,file, plugin = None):
		""" GUESS the output of single file """
		
		super(KMeans, self).predict(file, plugin)

		data = file.vector
		X = data[plugin]
		X = self.scaler.transform(X)
		guess = self.clf.predict(X)
		
		return self.getTag(guess)