from peewee import *
from datetime import datetime

from configure import *

database = MySQLDatabase(sql_db, **{'host':'localhost',
                                    'password':sql_pass,
                                    'port':3306,
                                    'user':sql_user})

class Song(Model):
    id = PrimaryKeyField()
    song_id = CharField()
    title = CharField()
    artist = CharField()
    album = CharField()
    cover = CharField()
    mp3 = CharField()
    ogg = CharField()
    lyric = CharField(null=True)
    update_at = DateTimeField(default=datetime.now)

    class Meta:
        database = database
