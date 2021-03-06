from soccerDB.application import db
import datetime


class Competition(db.EmbeddedDocument):
    id = db.IntField()
    name = db.StringField(max_length=200)
    url = db.StringField()


class Side(db.EmbeddedDocument):
    name = db.StringField(max_length=200)
    url = db.StringField()


class HighlightVideo(db.EmbeddedDocument):
    embed = db.StringField()
    title = db.StringField()


class SoccerInfo(db.Document):
    competition = db.EmbeddedDocumentField(Competition)
    date = db.StringField()
    embed = db.StringField()
    side1 = db.EmbeddedDocumentField(Side)
    side2 = db.EmbeddedDocumentField(Side)
    thumbnail = db.StringField()
    title = db.StringField()
    url = db.StringField()
    videos = db.EmbeddedDocumentListField(HighlightVideo)
    last_refreshed = db.DateTimeField(default=datetime.datetime.utcnow)
    user_id = db.IntField(required=False)
