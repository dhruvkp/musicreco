from MusicReco.models.db import *
import pandas as pd
from MusicReco.mllib import mllib
from utils import *
from sklearn.cross_validation import train_test_split

class Manager:
    """
        Manager to load music files, save feature vectors in DB.
    """

    def __init__(self, model, learner=None):
        self.model = model
        self.learner = learner
        self.mllib = mllib.mllib()
        self.pluginFilter = None

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

    def train(self, filter=None):
        """ Learning algorithms for audio classification """
        #Todo: Filter not implemented. Filter will make sure only 
        # Selected plugins are passed inside dataframe.
        files = Audio.select().filter(state=1).filter(istest=0)

        index = []
        rows = [] 
        for file in files:
            #print(file, file.vector, file.genre)
            row = {'class':file.genre}

            index.append(file.name)
            row.update(file.vector)

            rows.append(row)
        
        df = pd.DataFrame(index = index, data=rows)

        self.mllib.train(data= df)

    def test(self):
        return self.mllib.test(plugin=self.pluginFilter)

    def accuracy_score(self, p , n):
        print("ACCURACY SCORE ", p / (p + n ))

    def init_vectors(self, plugin= None, limit = 10):
        """ Apply plugins to music files """
        files  = Audio.select().filter(state=0).filter(istest=0).limit(limit)
        self.pluginFilter = plugin

        plugins = self.model.get_plugins(name=plugin)
        for plugin in plugins:
            for file in files:
                print(("PROCESSING ", file.name))
                plugin.process(file)

        #except Exception, e:
    #        print 'init_vectors manager.py ', e
