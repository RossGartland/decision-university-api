from models.university import University
from flask import Flask, request, jsonify, make_response, Response
from bson import ObjectId
from models.user import User
from models.bookmark import Bookmark
import datetime
from decorators.jwt_decorator import JWTDecorator
import jwt
import config
from mongoengine.errors import ValidationError
import pymongo
# Bookmarks


class BookmarkService():

    def __init__(self):
        self.users = User._get_collection()

    # Add a bookmark
    @JWTDecorator.jwt_required
    def add_new_bookmark(self, id):
        try:
            bookmark = Bookmark()  # Using the bookmark model
            bookmark.id = ObjectId()
            bookmark.institutionID = request.json["institutionID"]
            bookmark.institutionName = request.json["institutionName"]
            bookmark.crtdDateTime = datetime.datetime.utcnow()
            token = request.headers['x-access-token']
            # Get username from logged in user.
            data = jwt.decode(token, config.config['SECRET_KEY'])
            bookmark.username = data['user']

            findBookmark = self.users.find_one(
                {"_id": ObjectId(id), "bookmarks.institutionID": bookmark.institutionID})
            print(findBookmark)  # User can only bookmark a univesity once.

            if findBookmark is not None:
                return make_response(jsonify({"error": "Bookmark already exists for this university."}), 409)

            self.users.update_one({"_id": ObjectId(id)},
                                  {"$push": {"bookmarks": {
                                             "_id": bookmark.id,
                                             "institutionID": bookmark.institutionID,
                                             "institutionName": bookmark.institutionName,
                                             }}})

            return make_response(jsonify({"message": "Bookmark added",
                                          "url": "http://127.0.0.1:5000/api/v1.0/users/"+str(id)+"/bookmarks/"+str(bookmark.id)}), 201)
        except ValidationError:
            return make_response(jsonify({"error": "One or more fields contains invalid data."}), 403)
        except KeyError:
            return make_response(jsonify({"error": "One or more fields does not exist."}), 403)


# Get all bookmarks for an event

    @JWTDecorator.jwt_required
    def show_all_bookmarks_for_user(self, id):

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.config['SECRET_KEY'])

        # Prevent other users from seeing a users bookmarks.
        if data['user_id'] != id:
            return make_response(jsonify({"error": "User ID is invalid"}), 409)

        data_to_return = []
        page_num, page_size, sort = 1, 10, pymongo.DESCENDING
        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))
        page_start = (page_size * (page_num - 1))
        if request.args.get('sort') == "rankdesc":  # Get sorting criteria
            # Will show bookmarks in descending order first.
            sort = pymongo.DESCENDING
        elif request.args.get('sort') == "rankasc":
            sort = pymongo.ASCENDING

        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            # Generate seperate documents via $unwind.
            {"$unwind": "$bookmarks"},
            {"$sort": {"_id": 1, "bookmarks.sentDateTime": sort}},
            # Re-construct array by pushing bookmark objects.
            {"$group": {"_id": "$_id", "bookmarks": {"$push": "$bookmarks"}}},
            {"$skip": page_start},
            {"$limit": page_size},
        ]

        for user in self.users.aggregate(pipeline):
            user['_id'] = str(user['_id'])
            for bookmark in user["bookmarks"]:
                bookmark["_id"] = str(bookmark["_id"])
                data_to_return.append(bookmark)
        if len(data_to_return) > 0:
            return make_response(jsonify(data_to_return), 200)
        return make_response(jsonify({"error": "No Bookmarks found for user."}), 404)

# Get a single bookmark
    @JWTDecorator.jwt_required
    def show_bookmark_by_id(self, uid, bid):

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.config['SECRET_KEY'])

        # Prevent other users from seeing a users bookmarks.
        if data['user_id'] != uid:
            return make_response(jsonify({"error": "User ID is invalid"}), 409)

        user = self.users.find_one(
            {"bookmarks._id": ObjectId(bid)},
            {"_id": 0, "bookmarks.$": 1})
        if user is None:
            return make_response(
                jsonify(
                    {"error": "Invalid user ID or bookmark ID"}), 404)
        user['bookmarks'][0]['_id'] = \
            str(user['bookmarks'][0]['_id'])
        return make_response(jsonify(user['bookmarks'][0]), 200)

    # Get bookmark by institution name. Returns true if found.
    @JWTDecorator.jwt_required
    def show_bookmark_by_institution_id(self, uid, iid):

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.config['SECRET_KEY'])

        # Prevent other users from seeing a users bookmarks.
        if data['user_id'] != uid:
            return make_response(jsonify({"error": "User ID is invalid"}), 409)

        user = self.users.find_one(
            {"bookmarks.institutionID": iid},
            {"_id": 0, "bookmarks.$": 1})
        if user is None:
            return make_response(
                jsonify(
                    {"result": False}), 404)
        user['bookmarks'][0]['_id'] = \
            str(user['bookmarks'][0]['_id'])
        return make_response({"result": True}, 200)

# Delete a bookmark
    @JWTDecorator.jwt_required
    def remove_bookmark(self, uid, iid):

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.config['SECRET_KEY'])

        # Prevent other users from seeing a users bookmarks.
        if data['user_id'] != uid:
            return make_response(jsonify({"error": "User ID is invalid"}), 409)
        bookmark = self.users.find_one(
            {"bookmarks.institutionID": iid},
            {"_id": 0, "bookmarks.$": 1})

        self.users.update_one(
            {"_id": ObjectId(uid)},
            {"$pull": {"bookmarks":
                       {"institutionID": iid}}})
        return make_response(jsonify({}), 204)
