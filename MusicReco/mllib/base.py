from MusicReco.models.db import *
import MusicReco.models.db
import pandas as pd
import random
from config import settings
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch

class Base:
	def __init__(self):
		self.model = MusicReco.models.db
		self.__convert = lambda x: pd.Series([i for i in x])
		self.__ind = lambda x: self.getIndex(x)
		self.clf = None

	def process(self, limit=10, plugin = None, **filters):

		files  = self.model.get_audio_files(limit=limit,**filters)
		plugins = self.model.get_plugins(name=plugin)

		for file in files:
			print(("PROCESSING ", file.name))

			for plugin in plugins:
				plugin.process(file)

	def test(self, limit= 1000, plugin=None):
		""" Load data from test file & test
			Generate vectors where state = 0 and istest = 1
		"""

		self.process(limit=limit, plugin=plugin, state = 0,istest=1)
		return self.score(limit, plugin=plugin)

	def getDataFrame(self):
		""" Get the dataframe object from training where state = 1 and istest = 0 """
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

	def score(self, limit, plugin=None):
		positive = 0
		negative = 0

		files  = Audio.select().filter(istest=1).limit(limit)
		for file in files:
			guess = self.predict(file, plugin=plugin)
			print("guess -> ", guess, "Actual -> ", file.genre)

			if guess == file.genre:
				positive += 1
			else:
				negative += 1
				
		return (positive, negative)

	def train(self, data=None, plugin = None):
		if plugin is None:
			raise NameError("No plugin error. Can't train! ")

		X = data[plugin]
		# split the data in columns
		
		self.X_train = X.apply(self.__convert)

		# Combine X_train & Y_train
		self.X_train['class'] = data['class'].apply(self.__ind)


	def predict(self, file, plugin = None):
		if plugin not in file.vector:
			msg = "plugin output not found for file %s %s"%(file.name, plugin)
			raise NameError(msg)

		if self.clf is None:
			tags = settings['tags']
			guessid = random.randint(0, len(tags)-1)
			return tags[guessid]
			
	def getIndex(self, tag):
		return settings['tags'].index(tag)

	def getTag(self, ind):
		return settings['tags'][ind]

	def plot(self, data=None):
		#data = self.getDataFrame()
		fig = plt.figure(figsize=(7,7))
		ax = fig.add_subplot(111, projection='3d')
		for i in range(10):
			
			X = data[data[:,-1] == i]
			ax.plot(X[:,0],X[:,1],X[:,2],'o',color=np.random.rand(3,1), alpha=0.4, label='%s'%(settings['tags'][i]))
			
		plt.title('Transformed samples with class labels from matplotlib.mlab.PCA()')
		plt.legend()
		plt.show()

	def plot1(self, data=None):
		#data = self.getDataFrame()
		fig = plt.figure(figsize=(7,7))
		ax = fig.add_subplot(111, projection='3d')
		for i in range(10):
			
			X = data[data[:-1] == i]
			ax.plot(X[:,0],X[:,1],X[:,2],'o',color=np.random.rand(3,1), alpha=0.4, label='%s'%(settings['tags'][i]))
			
		plt.title('Transformed samples with class labels from matplotlib.mlab.PCA()')
		plt.legend()
		plt.show()