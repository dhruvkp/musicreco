from sklearn import svm
from sklearn.preprocessing import StandardScaler

from .base import Base

class SVM(Base):

	def train(self, data = None):
		""" With dataframe train mllib """
		X = data['GMM'].tolist()
		self.clf = svm.SVC(gamma=0.001, C= 100.)

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