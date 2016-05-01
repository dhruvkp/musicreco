from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA as sklearnPCA

from .base import Base

class SVM(Base):

	def train(self, data = None, plugin=None):
		""" With dataframe train mllib """
		super(SVM, self).train(data, plugin)
		
		self.clf = svm.SVC(gamma=0.001, C= 5,  kernel='rbf')
		#self.clf = svm.LinearSVC(C=10, loss='squared_hinge', penalty='l2', tol=0.00001)
		X = self.X_train.iloc[:,:-1]
		Y = self.X_train.iloc[:,-1]

		self.scaler = StandardScaler().fit(X)
		#self.scaler = sklearnPCA(n_components=60).fit(X)
		X = self.scaler.transform(X)

		self.clf.fit(X, Y)

	def predict(self, file, plugin=None):
		super(SVM, self).predict(file, plugin)

		data = file.vector
		X = data[plugin]
		X = self.scaler.transform(X)
		guess = self.clf.predict(X)
		return self.getTag(guess)