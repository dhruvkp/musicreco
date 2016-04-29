from sklearn import svm
from utils import *
from MusicReco.models.db import *
import MusicReco.models.db


class mllib:
	def __init__(self):
		self.model = MusicReco.models.db

	def train(self, data = None):
		""" With dataframe train mllib """
		self.clf = svm.SVC(gamma=0.001, C= 100.)
		print(data['class'])
		self.clf.fit(data['fextract'].tolist(), data['class'].tolist())

	def test(self, limit= 2, plugin=None):
		""" Load data from test file & test """
		files  = Audio.select().filter(istest=1).limit(limit)

		plugins = self.model.get_plugins(name=plugin)
		
		for file in files:
			print(("TEST PROCESSING ", file.name))

			for plugin in plugins:
				plugin.process(file)

            # create dataframe and test
			data = file.vector
			print("GUESS -> ", self.clf.predict(data['fextract'].tolist()))