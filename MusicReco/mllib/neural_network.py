from sklearn import svm
from sklearn.preprocessing import StandardScaler

from .base import Base
from sklearn.neural_network import MLPClassifier

class Neural(Base):

	def train(self, data = None):
		""" With dataframe train mllib """
		X = data['GMM'].tolist()
		self.clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(10, 3), random_state=1)

		#import pdb
		#pdb.set_trace()
		self.scaler = StandardScaler().fit(X)
		X = self.scaler.transform(X)
		self.clf.fit(X, data['class'].tolist())

	def predict(self, file):
		data = file.vector
		X = data['GMM'].tolist()
		X = self.scaler.transform(X)
		return self.clf.predict(X)