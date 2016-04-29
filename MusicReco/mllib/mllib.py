from sklearn import svm
from utils import *
from MusicReco.models.db import *
import MusicReco.models.db
from sklearn.preprocessing import StandardScaler

class mllib:
	def __init__(self):
		self.model = MusicReco.models.db

	def train(self, data = None):
		""" With dataframe train mllib """
		self.clf = svm.SVC(gamma=0.001, C= 100.)

		self.scaler = StandardScaler().fit(data['fextract'].tolist())
		X = self.scaler.transform(data['fextract'].tolist())
		self.clf.fit(X, data['class'].tolist())

	def test(self, limit= 10, plugin=None):
		""" Load data from test file & test """
		files  = Audio.select().filter(istest=1).limit(limit)

		plugins = self.model.get_plugins(name=plugin)
		positive = 0
		negative = 0

		for file in files:
			print(("TEST PROCESSING ", file.name))

			for plugin in plugins:
				plugin.process(file)

            # create dataframe and test
			data = file.vector
			X = self.scaler.transform(data['fextract'].tolist())
			guess = self.clf.predict(X)
			print("GUESS -> ", guess, "ACTUAL -> ", file.genre)

			if(guess == file.genre):
				positive += 1
			else:
				negative += 1

		return (positive, negative)