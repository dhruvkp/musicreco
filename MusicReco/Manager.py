from MusicReco.models.db import *
import pandas as pd
from MusicReco.mllib.KMeans import KMeans
from MusicReco.mllib.KNN import KNN
from MusicReco.mllib.svm import SVM
from MusicReco.mllib.linear import Linear
from MusicReco.mllib.ada_boost import ADABoost
# from MusicReco.mllib.neural_network import Neural
from utils import *
from sklearn.cross_validation import train_test_split
from sklearn.decomposition import PCA as sklearnPCA
import numpy as np
import sklearn.metrics as metrics
from sklearn.metrics import confusion_matrix, classification_report
from config import settings


import matplotlib.pyplot as plt
class Manager:
    """
        Manager to load music files, save feature vectors in DB.
    """

    def __init__(self, model, learner=None):
        self.model = model
        self.learner = learner
        self.mllib  = None
        self.pluginFilter = None

    def use_ml(self, ml = None):
        if ml == "ANN":
            self.mllib = Neural()
        elif ml == "SVM":
            self.mllib = SVM()
        elif ml == "KMEANS":
            self.mllib = KMeans()
        elif ml == "KNN":
            self.mllib = KNN()
        elif ml == "ADABOOST":
            self.mllib = ADABoost()
        elif ml == "LINEAR":
            self.mllib = Linear()

    def use_plugin(self, plugin):
        self.pluginFilter = plugin

    def add_plugin(self, name, module_name):
        Plugin.get_or_create(name=name, module_name = module_name)

    def initialize_storage(self):
        self.model.create_tables()

    def add_tag(self, tag):
        return Tag.get_or_create(genre = tag)[0]

    def add_file(self, path, file_name, tag, istest=0):
        t = self.add_tag(tag)
        Audio.get_or_create(name = file_name, path = path, tag = t, istest=istest)

    def load_collection(self, tags, dirname, test_size=0.33):
        files = load_collection(tags, dirname)
        train_files, test_files = train_test_split(files, test_size = test_size, random_state=42)

        for path, file, tag in train_files:
            self.add_file(path, file, tag)

        for path, file, tag in test_files:
            self.add_file(path, file, tag, istest=1)


    def load_plugins(self, plugins):
       for name, plugin in plugins.items():
            self.add_plugin(name, plugin)

    def train(self):
        """ Learning algorithms for audio classification """
        #Todo: Filter not implemented. Filter will make sure only
        # Selected plugins are passed inside dataframe.

        df = self.mllib.getDataFrame()

        self.mllib.train(data= df, plugin = self.pluginFilter)

    def test(self):
        return self.mllib.test(plugin=self.pluginFilter)

    def plot(self):

        self.train()
        # this will get data frame in self.mllib.X_train
        X = self.mllib.X_train.iloc[:,:-1]
        Y = self.mllib.X_train.iloc[:,-1]

        # get data in 3D axis
        scaler = sklearnPCA(n_components=3).fit(X)
        X = scaler.transform(X)
        Y = Y.reshape(Y.shape[0],1)
        X = np.append(X, Y, 1)

        self.mllib.plot(X)

    def plot_confusion_matrix(self,cm, title='Confusion matrix', cmap=plt.cm.Blues):
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(settings['tags']))
        plt.xticks(tick_marks, settings['tags'], rotation=45)
        plt.yticks(tick_marks, settings['tags'])
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.savefig("result.jpg")


    def accuracy_score(self, predict , test):
        """ GET accuracy score """
        #TODO: Extend it to confusion matrix
        #print("ACCURACY SCORE ", p / (p + n ))
        print(metrics.classification_report(test, predict, target_names = settings['tags']))

        print(metrics.accuracy_score(test, predict))

        cm = metrics.confusion_matrix(test, predict)
        self.plot_confusion_matrix(cm)



    def init_vectors(self,limit = 10):
        """ Apply plugins to music files """
        # process all files with state = 0 and no test files
        self.mllib.process(plugin=self.pluginFilter, limit=limit, state=0, istest=0)
