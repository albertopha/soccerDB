import requests
from flask import Blueprint, jsonify
from soccerDB.application.model import User, SoccerInfo
from flask_restplus import Api, Resource

blueprint = Blueprint('api_routes', __name__)
api_routes = Api(blueprint)


############## /api/v1/soccerinfos ###############

@api_routes.route('/v1/soccerinfos')
class V1SoccerInfosApi(Resource):
    url = "https://www.scorebat.com/video-api/v1/"

    def get(self):
        response = requests.get(self.url)
        return jsonify(response.json())

    # def post(self):
    #     response = requests.get(self.url)
    #

##################################################


################# /api/v1/users ##################

@api_routes.route('/v1/users')
class V1UsersApi(Resource):

    def get(self):
        """
        Retrieve all users
        :return: all users
        """
        print(User.objects.all())
        return jsonify(User.objects.all())

    def post(self):
        """
        Creates a user
        :return: void
        """
        user1 = User(user_id=4, first_name="Albert4", last_name="Oh2", email="albert@email.com", password="password")
        print(user1)
        user1.save()
        return jsonify({"message": "successfully created!"})

##################################################
