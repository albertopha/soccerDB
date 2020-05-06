import requests
from _datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from soccerDB.application.model import User, SoccerInfo
from flask_restplus import Api, Resource

from soccerDB.application.model.SoccerInfo import Side, HighlightVideo, Competition

blueprint = Blueprint('api_routes', __name__)
api_routes = Api(blueprint)

storage = dict(
    cached_soccerInfos=[]
)

############## /api/v1/soccerinfos ###############
@api_routes.route('/v1/soccerinfos')
class V1SoccerInfos(Resource):
    url = "https://www.scorebat.com/video-api/v1/"

    def get(self):
        """
        Fetches/Refreshes soccerInfo (when last_refreshed is over a day)
        :return: Json with most recent soccerInfos
        """
        # Check if last_refreshed is saved in the storage
        if "last_refreshed" in storage:
            self.refresh_infos(storage["last_refreshed"])
        else:
            # last_refreshed not found in the storage
            soccerInfo = SoccerInfo.objects.first()
            if soccerInfo and soccerInfo["last_refreshed"]:
                self.refresh_infos(soccerInfo["last_refreshed"])
            else:
                self.refresh_infos()
        return storage["cached_soccerInfos"], 200

    def refresh_infos(self, saved_time=None):
        current_time = datetime.utcnow()
        new_soccerInfos = requests.get(self.url).json()
        if not saved_time:
            self.save_soccerInfos(new_soccerInfos, True)
        elif current_time > saved_time + timedelta(days=1):
            self.save_soccerInfos(new_soccerInfos)

        soccer_infos = jsonify(SoccerInfo.objects.all()).get_json()
        if soccer_infos and len(soccer_infos) > 0:
            storage["last_refreshed"] = soccer_infos[0]["last_refreshed"]
            storage["cached_soccerInfos"] = soccer_infos

    def save_soccerInfos(self, soccerInfos, skip_drop=False):
        """
        Stores list of soccer Infos into MongoDB
        :param soccerInfos: list of soccer infos
        :return: None
        """
        # Drops existing collection to prevent conflicts
        if not skip_drop:
            SoccerInfo.drop_collection()

        # Refill collection with new SoccerInfo documents
        for info in soccerInfos:
            competition = Competition(
                id=info["competition"]["id"],
                name=info["competition"]["name"],
                url=info["competition"]["url"]
            )

            side1 = Side(name=info["side1"]["name"], url=info["side1"]["url"])
            side2 = Side(name=info["side2"]["name"], url=info["side2"]["url"])

            videos = []
            for video in info["videos"]:
                highlight = HighlightVideo(embed=video["embed"], title=video["title"])
                videos.append(highlight)

            soccerInfo = SoccerInfo(
                competition=competition,
                date=info["date"],
                embed=info["embed"],
                side1=side1,
                side2=side2,
                thumbnail=info["thumbnail"],
                title=info["title"],
                url=info["url"],
                videos=videos,
                last_refreshed=datetime.utcnow(),
                user_id=None
            )

            soccerInfo.save()


@api_routes.route('/v1/soccerinfos/favorites/<user_id>')
class V1SoccerInfosFavorites(Resource):

    def get(self, user_id):
        user = User.objects(user_id__exact=user_id)
        return user.favourites

    def post(self, user_id):
        user = User.objects(user_id__exact=user_id)
        ids = request.get_json()["ids"]
        soccer_infos = []
        for id in ids:
            soccer_info = SoccerInfo.objects(id__exact=id)
            soccer_infos.append(soccer_info)

        user["favourites"].extend(soccer_infos)
        user.update(set__favourites=user["favourites"])
        return 201


################# /api/v1/users ##################

@api_routes.route('/v1/users')
class V1UsersList(Resource):

    def get(self):
        """
        Retrieve all users
        :return: all users
        """
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
        """
        Retrieve single user by user_id
        :param user_id: user id
        :return: Json
        """
        return jsonify(User.objects(user_id__exact=user_id))

    def put(self, user_id):
        """
        TODO: cascading update to soccerInfo for user_id change
        Updates entire User
        :param user_id: user id
        :return: message dict
        """
        try:
            data = request.get_json()
            date = datetime.fromtimestamp(data['last_login']['$date'] / 1e3)
            user = User.objects(user_id__exact=user_id)
            user.update(
                set__user_id=data['user_id'],
                set__first_name=data['first_name'],
                set__last_name=data['last_name'],
                set__email=data['email'],
                set__password=data['password'],
                set__last_login=date
            )
            return {"message": "successfully updated!"}, 201
        except Exception as err:
            return {"message": "Failed to update: {0}".format(err)}, 405

    def patch(self, user_id):
        """
        TODO: cascading update to soccerInfo for user_id change
        Updates fields of the User
        :param user_id: user id
        :return: message dict
        """
        data = request.get_json()
        try:
            user = User.objects(user_id__exact=user_id)

            if 'user_id' in data:
                user.update(set__user_id=data['user_id'])

            if 'first_name' in data:
                user.update(set__first_name=data['first_name'])

            if 'last_name' in data:
                user.update(set__last_name=data['last_name'])

            if 'email' in data:
                user.update(set__email=data['email'])

            if 'password' in data:
                user.update(set__password=data['password'])

            if 'last_login' in data:
                date = datetime.fromtimestamp(data['last_login']['$date'] / 1e3)
                user.update(set__last_login=date)

            return {"message": "successfully patched!"}, 201
        except Exception as err:
            return {"message": "Failed to patch: {0}".format(err)}, 405

    def delete(self, user_id):
        """
        TODO: cascading delete to soccerInfo for user_id change
        Deletes user and corresponding soccerInfo
        :param user_id:
        :return:
        """
        user = User.objects(user_id__exact=user_id)
        user.delete()

##################################################
