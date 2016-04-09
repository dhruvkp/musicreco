from peewee import *
from playhouse.fields import PickledField

database = SqliteDatabase('wee.db')

class Artist(Model):
	name = CharField()
	class Meta:
		database = database

class Album(Model):
	artist = ForeignKeyField(Artist)
	title = CharField()
	release_date = DateTimeField()
	publisher = CharField()
	media_type = CharField()
	data = PickledField(null=True)
	
	class Meta:
		database = database

if __name__ == '__main__':
	try:
		Artist.create_table()
	except:
		print "Artist table already exists"
	
	try:
		Album.create_table()
	except:
		print "Album table already exists"

