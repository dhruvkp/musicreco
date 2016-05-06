from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from .base import Base

class Linear(Base):

	def train(self, data = None, plugin=None):
		""" With dataframe train mllib """
		super(Linear, self).train(data, plugin)
		self.clf = GaussianNB()
		X = self.X_train.iloc[:,:-1]
		Y = self.X_train.iloc[:,-1]

		self.scaler = StandardScaler().fit(X)
		X = self.scaler.transform(X)
		self.clf.fit(X, Y)

	def predict(self, file, plugin=None):
		super(Linear, self).predict(file, plugin)

		data = file.vector
		X = data[plugin]
		X = self.scaler.transform(X)
		guess =  self.clf.predict(X)
		return self.getTag(guess)
