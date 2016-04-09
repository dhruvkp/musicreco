import peewee
from playhouse.kv import PickledField

from models import Album, Artist

band = Artist.select().where(Artist.name == "Kutless").get()
print band.name

first_album = Album.get()
print first_album.data
