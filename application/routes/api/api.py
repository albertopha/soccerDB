import requests
from flask import Blueprint, jsonify
from soccerDB.application.model import User
from flask_restplus import Resource

api_routes = Blueprint('app_routes', __name__)

url = "https://www.scorebat.com/video-api/v1/"


@api_routes.route('/')
def api():
    response = requests.get(url)
    return jsonify(response.json())

@api_routes.route('/soccerinfos')
def get_all_soccer_infos():
    user1 = User(user_id=4, first_name="Albert4", last_name="Oh2", email="albert@email.com", password="password")
    print(user1)
    user1.save()
    users = User.objects.all()
    return jsonify(users)
    # response = User.objects.all()
    # print(response)
    # return jsonify(response)
