from flask import Blueprint

api_routes = Blueprint('app_routes', __name__)
@api_routes.route('/')
def api():
    return '<h1>API CALLED</h1>'