import requests
from flask import Blueprint, jsonify, request
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
class V1UsersList(Resource):

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
        data = request.get_json()
        try:
            user = User(
                user_id=data['user_id'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password']
            )
            user.save()
            return {"message": "successfully created!"}, 201
        except Exception as err:
            return {"message": "Failed to create: {0}".format(err)}, 405


@api_routes.route('/v1/users/<user_id>')
class V1Users(Resource):

    def get(self, user_id):
        return jsonify(User.objects(user_id__exact=user_id))


##################################################
