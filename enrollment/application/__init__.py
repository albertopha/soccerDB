from flask import Flask
from enrollment.application.routes import api_routes, view_routes

app = Flask(__name__)


print(app.url_map)

app.register_blueprint(view_routes, url_prefix='/views')
app.register_blueprint(api_routes, url_prefix='/api')
