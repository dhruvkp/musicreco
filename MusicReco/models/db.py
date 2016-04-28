from peewee import *
from playhouse.kv import PickledField
import MusicReco.models.abstract as abstract
from config import settings
import os
from collections import defaultdict
# Config - aside from our database

DATABASE = settings['db']['database']

database = SqliteDatabase(DATABASE)

# model definitions -- the standard "pattern"
class BaseModel(Model):
    class Meta:
        database = database

# User model specifies its fields
class Plugin(BaseModel, abstract.Plugin):
    name = CharField(unique = True)
    module_name = CharField()

    def createVector(self, audio):
        return PluginOutput(vector = self.module.createVector(audio.path),
                        plugin = self,
                        audio = audio )

    def process(self, file):
        update_vector(self, file)
        file.state = 1
        file.save()

class Tag(BaseModel, abstract.Tag):
    genre = CharField()

class Audio(BaseModel, abstract.Audio):
    name = CharField()
    path = CharField()
    tag = ForeignKeyField(Tag, related_name = 'audio', null=True)
    state = IntegerField(null=True, default=0)
    # We can extend it further by adding numplayed, star

    def process(self, plugin):
        update_vector(plugin, self)
        self.state = 1
        self.save()

    def plugin_outputs(self):
        result= {}
        if self.state == 0:
            print("Not processed yet..")
        for pout in self.poutputs:
            result[pout.plugin.name] = pout.vector
        return result

class PluginOutput(BaseModel, abstract.PluginOutput):
    plugin = ForeignKeyField(Plugin)
    audio = ForeignKeyField(Audio, related_name='poutputs')
    vector = PickledField()

    def __repr__(self):
        return "<Pluging Output %d %d>: "%(self.plugin.id, self.audio.id),self.vector

class Cluster(BaseModel):
    tag = ForeignKeyField(Tag, related_name = 'clusters')
    audio = ForeignKeyField(Audio, related_name ='clusters')

def create_tables():
    directory = os.path.dirname(DATABASE)
    if not os.path.exists(directory):
      os.makedirs(directory)

    database.connect()
    try:
        database.create_tables([Plugin, Audio, Cluster, Tag, PluginOutput])
    except:
        print("Database already created. Skipping it")

def get_plugins(name = None, module_name = None):
    """ Returns a list of plugin objects. By default returns all plugins.
    @param name : if provided, returns only plugins with a matching name
    @type name  : unicode

    @param module_name : if provided, returns only plugins with matching name
    @type  module_name : unicode
    """
    query = Plugin.select()
    if name != None:
        query = query.filter(Plugin.name == name)

    if module_name != None:
        query = query.filter(Plugin.module_name == module_name)

    return query

def get_audio_files( file_name = None, tag = None):
    query = Audio.select().where(Audio.file_name == file_name)

    if tag != None:
        query = query.join(Tag).filter(Tag.genre == tag)

    return query

def update_vector(plugin , audio):
    """ Create or replace the current plugin output object for the provided plugin/audio file pair """

    old_output = PluginOutput.select(Plugin, Audio ).join(Plugin, on=(Plugin.id == PluginOutput.plugin_id) ).join(Audio, on=( Audio.id == PluginOutput.audio_id))

    try:
        old_output.get()
        old_output.delete_instance()
    except Exception as e:
        pass

    PO = plugin.createVector(audio)
    PO.save()
    
    return PO
