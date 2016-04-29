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
    guess = CharField(null=True)
    istest = BooleanField(default=0, null=False)
    # We can extend it further by adding numplayed, star

    def process(self, plugin):
        update_vector(plugin, self)
        self.state = 1
        self.save()


class PluginOutput(BaseModel, abstract.PluginOutput):
    plugin = ForeignKeyField(Plugin)
    audio = ForeignKeyField(Audio, related_name='poutputs')
    vector = PickledField()

    def __repr__(self):
        return "<Pluging Output %d %d>: "%(self.plugin.id, self.audio.id)

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

def get_audio_files( limit= 10, **filters):
    query = Audio.select()

    if len(filters):
        query = query.filter(**filters)

    query = query.limit(limit)

    return query

def update_vector(plugin , audio):
    """ Create or replace the current plugin output object for
         the provided plugin/audio file pair """

    PO = plugin.createVector(audio)
    PO.save()
    
    return PO
