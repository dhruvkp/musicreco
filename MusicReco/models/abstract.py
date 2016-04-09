import os

class Plugin(object):
    """ Plugin object to create music feature vector
        Attributes: name
                    module_name
                    outputs

        Methods:
            createVector
    """
    def __init__(self, name, module_name):
        self.name = name
        self.module_name = module_name
        self.outputs = []

    def __getattr__(self, name):
        if name == 'module':
            # Lazy load the plugin module
            if 'module' not in self.__dict__:
                print "magic function ", self.module_name
                mod = __import__(self.module_name)
                components = self.module_name.split('.')
                for comp in components[1:]:
                    mod = getattr(mod, comp)

                self.__dict__["module"] = mod
            return self.__dict__["module"]

        else:
            return object.__getattr__(name)

    def __repr__(self):
        return "<Plugin('%s', '%s')" %(self.name, self.module_name)

    def createVector(self, audio):
        return PluginOutput(self.module.createVector(audio.path), self, audio)


class Audio(object):
    """ Audio file object
    Attributes:
        name
        vector
        tag
    """

    def __init__(self, file_name, tag=None):
        self.file_name = file_name
        self.vector = []
        self.tag = tag

    def __repr__(self):
        return "<AudioFile('%s')>"%(self.file_name)

class Tag(object):
    """ Tag Object and its representations """
    def __init__(self, name):
        self.name = name
        self.vector = []

    def __repr__(self):
        return "<Tag('%s')>"%(self.name)

class PluginOutput(object):
    """ Object to represent the output of plugin """

    def __init__(self, vector, plugin, audio):
        self.vector = vector
        self.plugin = plugin
        self.audio = audio

    def __repr__(self):
        return "<Plugin output ('%s')>" %(self.vector)
