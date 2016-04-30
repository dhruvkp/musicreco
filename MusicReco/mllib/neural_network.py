from sklearn import svm
from sklearn.preprocessing import StandardScaler

from .base import Base
from sklearn.neural_network import MLPClassifier

class Neural(Base):

	def train(self, data = None, plugin = None):
		""" With dataframe train mllib """
		super(Neural, self).train(data, plugin)
		
		X = X_train.iloc[:,:-1]
		Y = X_train.iloc[:,-1]

		self.clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(10, 3), random_state=1)

		self.scaler = StandardScaler().fit(X)
		X = self.scaler.transform(X)
		self.clf.fit(X, Y)

	def predict(self, file, plugin = None):
		super(Neural, self).predict(file, plugin)

		data = file.vector
		X = data[plugin]
		X = self.scaler.transform(X)
		guess = self.clf.predict(X)
		return self.getTag(guess)
