from soccerDB.application import db
from . import Competition, Side, HighlightVideo
import datetime


class SelectedSoccerInfo(db.EmbeddedDocument):
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


class SoccerInfoCollections(db.Document):
    favorites = db.ListField(db.EmbeddedDocumentField(SelectedSoccerInfo))
