import requests
from flask import Blueprint, jsonify


api_routes = Blueprint('app_routes', __name__)

url = "https://www.scorebat.com/video-api/v1/"


@api_routes.route('/')
def api():
    response = requests.get(url)
    return jsonify(response.json())
