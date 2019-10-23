from flask import Flask
from soccerDB.config import Config
from flask_mongoengine import MongoEngine
from soccerDB.application.routes import api_routes, view_routes

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)

print(app.url_map)

app.register_blueprint(view_routes, url_prefix='/views')
app.register_blueprint(api_routes, url_prefix='/api')
