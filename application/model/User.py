from soccerDB.application import db
from . import SoccerInfo
from datetime import datetime


class User(db.Document):
    user_id = db.StringField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30)
    password = db.StringField(max_length=30)
    last_login = db.DateTimeField(default=datetime.utcnow)
    favourites = db.ListField(SoccerInfo)
