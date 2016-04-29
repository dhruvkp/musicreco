from sklearn import svm
from sklearn.preprocessing import StandardScaler

from .base import Base

class Linear(Base):

	def train(self, data = None):
		""" With dataframe train mllib """
		self.clf = svm.SVC(gamma=0.001, C= 100.)

		self.scaler = StandardScaler().fit(data['fextract'].tolist())
		X = self.scaler.transform(data['fextract'].tolist())
		self.clf.fit(X, data['class'].tolist())

	def predict(self, file):
		data = file.vector
		X = data['fextract'].tolist()
		X = self.scaler.transform(X)
		return self.clf.predict(X)