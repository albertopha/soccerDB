from flask import Flask
from soccerDB.config import Config
from flask_mongoengine import MongoEngine
from flask_restplus import Api

api = Api()

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)
api.init_app(app)


from .routes import api_routes, view_routes
print(app.url_map)

app.register_blueprint(api_routes, url_prefix='/api')
app.register_blueprint(view_routes, url_prefix='/views')
