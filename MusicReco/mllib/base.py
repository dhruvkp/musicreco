from MusicReco.models.db import *
import MusicReco.models.db
import pandas as pd

class Base:
	def __init__(self):
		self.model = MusicReco.models.db

	def process(self, limit=10, plugin = None, **filters):

		files  = self.model.get_audio_files(**filters)
		#for k,v in filters.items():
		#	files = files.filter()
		plugins = self.model.get_plugins(name=plugin)

		for file in files:
			print(("TEST PROCESSING ", file.name))

			for plugin in plugins:
				plugin.process(file)


	def test(self, limit= 10, plugin=None):
		""" Load data from test file & test """
		self.process(limit, plugin, istest=1)
		return self.score(limit)

	def getDataFrame(self):
		files = Audio.select().filter(state=1).filter(istest=0)

		index = []
		rows = [] 
		for file in files:
			row = {'class':file.genre}

			index.append(file.name)
			row.update(file.vector)

			rows.append(row)

		df = pd.DataFrame(index = index, data=rows)
		return df

	def score(self, limit):
		positive = 0
		negative = 0

		files  = Audio.select().filter(istest=1).limit(limit)
		for file in files:
			guess = self.predict(file)

			if guess == file.genre:
				positive += 1
			else:
				negative += 1
				
		return (positive, negative)
