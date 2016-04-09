from MusicReco.models.db import *

class Manager:
    """
        Manager to load music files, save feature vectors in DB.
    """

    def __init__(self, model, learner=None):
        self.model = model
        self.learner = learner

    def add_plugin(self, name, module_name):
        Plugin.get_or_create(name=name, module_name = module_name)

    def initialize_storage(self):
        self.model.create_tables()

    def add_tag(self, tag):
        return Tag.get_or_create(genre = tag)[0]

    def add_file(self, path, file_name, tag):
        t = self.add_tag(tag)
        Audio.get_or_create(name = file_name, path = path, tag = t)

    def init_vectors(self, plugin= None, limit = 10):
        """ Apply plugins to music files """
        files  = Audio.select().filter(state=0).limit(limit)

        plugins = self.model.get_plugins(name=plugin)
        for plugin in plugins:
            for file in files:
                print(("PROCESSING ", file.name))
                po = self.model.update_vector(plugin, file)

                if file.vector == None:
                    file.vector = {}

                file.vector.setdefault(plugin.name, []).append(po.vector)
                file.state = 1                       # DONE PROCESSING
                file.save()

        #except Exception, e:
    #        print 'init_vectors manager.py ', e
