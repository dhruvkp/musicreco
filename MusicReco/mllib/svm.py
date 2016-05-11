from sklearn import svm
from sklearn.preprocessing import StandardScaler

from .base import Base
import numpy as np

class SVM(Base):

	def train(self, data = None, plugin=None):
		""" With dataframe train mllib """
		super(SVM, self).train(data, plugin)

		#self.clf = svm.SVC(gamma=0.001, C= 100, kernel='rbf')
		self.clf = svm.LinearSVC(C=10, loss='squared_hinge', penalty='l2', tol=0.00001)
		X = self.X_train.iloc[:,:-1]
		Y = self.X_train.iloc[:,-1]

		self.scaler = StandardScaler().fit(X)
		X = self.scaler.transform(X)

		# ONLY FOR PLOTTING
		# self.scaler = sklearnPCA(n_components=3).fit(X)
		# X = self.scaler.transform(X)
		# Y = Y.reshape(Y.shape[0],1)
		# X = np.append(X, Y, 1)
		# self.plot(X)
		# X = X[:,:-1]
		# # IT ENDS HERE

		self.clf.fit(X, Y)

	def predict(self, file, plugin=None):
		super(SVM, self).predict(file, plugin)

		data = file.vector
		X = data[plugin]
		X = self.scaler.transform(X)
		guess = self.clf.predict(X)
		return self.getTag(guess)
