from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.preprocessing import StandardScaler

from .base import Base

class ADABoost(Base):

	def train(self, data = None, plugin=None):
		""" With dataframe train mllib """
		super(ADABoost, self).train(data, plugin)
		
		self.clf = AdaBoostClassifier()

		X = self.X_train.iloc[:,:-1]
		Y = self.X_train.iloc[:,-1]

		self.scaler = StandardScaler().fit(X)
		X = self.scaler.transform(X)

		self.clf.fit(X, Y)

	def predict(self, file, plugin=None):
		super(ADABoost, self).predict(file, plugin)

		data = file.vector
		X = data[plugin]
		X = self.scaler.transform(X)
		guess = self.clf.predict(X)
		return self.getTag(guess)