from .base import Base
from sklearn.mixture import GMM
import numpy as np
import pandas as pd

class KMeans(Base):

	def __init__(self):
		self.__convert = lambda x: pd.Series([i for i in x])
		self.__ind = lambda x: self.getIndex(x)
		super(KMeans, self).__init__()

	def train(self, data=None):
		""" Training through KMeans """
		X = data['GMM']
		# split the data in columns

		X_train = data['GMM'].apply(self.__convert)

		# Combine X_train & Y_train
		X_train['class'] = data['class'].apply(self.__ind)

		# It contains only N X M mfcc matrix
		n_classes = len(np.unique(X_train['class']))

		# create 10 clusters
		self.clf = GMM(n_components = n_classes, init_params='wc', n_iter=20)

		# Initialize clf with each class mean
		self.clf.means_ = np.array([ X_train[X_train['class'] == i].iloc[:,:-1].mean(axis=0) for i in range(n_classes)])

		self.clf.fit(X_train.iloc[:,:-1], X_train.iloc[:,-1])

	def predict(self,file):
		""" GUESS the output of single file """
		# TODO: Unimplemented, Using random guess
		data = file.vector
		X = data['GMM']
		guess = self.clf.predict(X)

		return self.getTag(guess)