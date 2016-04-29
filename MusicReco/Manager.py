from MusicReco.models.db import *
import pandas as pd
from MusicReco.mllib.linear import Linear
from MusicReco.mllib.KMeans import KMeans
from utils import *
from sklearn.cross_validation import train_test_split

class Manager:
    """
        Manager to load music files, save feature vectors in DB.
    """

    def __init__(self, model, learner=None):
        self.model = model
        self.learner = learner
        #self.mllib = Linear()
        self.mllib  = KMeans()
        self.pluginFilter = None

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

        self.mllib.train(data= df)

    def test(self):
        return self.mllib.test(plugin=self.pluginFilter)

    def accuracy_score(self, p , n):
        """ GET accuracy score """
        #TODO: Extend it to confusion matrix
        print("ACCURACY SCORE ", p / (p + n ))

    def init_vectors(self,limit = 10):
        """ Apply plugins to music files """
        # process all files with state = 0 and no test files
        print("TRAINING AUDIO", limit)
        self.mllib.process(plugin=self.pluginFilter, limit=limit, state=0, istest=0)