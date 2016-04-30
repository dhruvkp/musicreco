from .base import Base
from sklearn.mixture import GMM
import numpy as np
import pandas as pd

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
		self.clf = GMM(n_components = n_classes, init_params='wc', n_iter=30, n_init=10)

		# Initialize clf with each class mean
		self.clf.means_ = np.array([ self.X_train[self.X_train['class'] == i].iloc[:,:-1].mean(axis=0) for i in range(n_classes)])

		self.clf.fit(X, Y)

	def predict(self,file, plugin = None):
		""" GUESS the output of single file """
		
		super(KMeans, self).predict(file, plugin)

		data = file.vector
		X = data[plugin]
		guess = self.clf.predict(X)
		
		return self.getTag(guess)