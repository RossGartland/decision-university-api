from models.university import University
from flask import Flask, request, jsonify, make_response, Response
from bson import ObjectId
from models.comments import Comment
import datetime
from decorators.jwt_decorator import JWTDecorator
import jwt
import config
from mongoengine.errors import ValidationError
import pymongo
# Comments


class CommentService():
    # Add a comment

    def __init__(self):
        self.universities = University._get_collection()

    @JWTDecorator.jwt_required
    def add_new_comment(self, id):
        try:
            comment = Comment()  # Using the comment model
            comment.id = ObjectId()
            comment.text = request.form["text"]
            comment.sentDateTime = datetime.datetime.utcnow()
            comment.isEdited = False
            comment.likeReactions = []
            comment.laughReactions = []
            comment.angryReactions = []
            token = request.headers['x-access-token']
            # Get username from logged in user.
            data = jwt.decode(token, config.config['SECRET_KEY'])
            comment.username = data['user']
            comment.user_id = data['user_id']

            self.universities.update_one({"_id": ObjectId(id)},
                                         {"$push": {"comments": {
                                             "_id": comment.id,
                                             "username": comment.username,
                                             "text": comment.text,
                                             "sentDateTime": comment.sentDateTime,
                                             "isEdited": comment.isEdited,
                                             "likeReactions": comment.likeReactions,
                                             "laughReactions": comment.laughReactions,
                                             "angryReactions": comment.angryReactions,
                                             "user_id": comment.user_id,
                                         }}})

            return make_response(jsonify({"message": "Comment added",
                                          "url": "http://127.0.0.1:5000/api/v1.0/users/"+str(id)+"/comments/"+str(comment.id)}), 201)
        except ValidationError:
            return make_response(jsonify({"error": "One or more fields contains invalid data."}), 403)
        except KeyError:
            return make_response(jsonify({"error": "One or more fields does not exist."}), 403)


# Get all comments for an university


    def show_all_comments(self, id):

        data_to_return = []
        page_num, page_size, sort = 1, 5, pymongo.DESCENDING
        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))
        page_start = (page_size * (page_num - 1))
        if request.args.get('sort') == "rankdesc":  # Get sorting criteria
            # Will show comments in descending order first.
            sort = pymongo.DESCENDING
        elif request.args.get('sort') == "rankasc":
            sort = pymongo.ASCENDING

        count = self.universities.find_one({"_id": ObjectId(id)},
                                           {"comments": 1})
        print(len(count["comments"]))
        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            # Generate seperate documents via $unwind.
            {"$unwind": "$comments"},
            {"$sort": {"_id": 1, "comments.sentDateTime": sort}},
            {"$skip": page_start},
            {"$limit": page_size},
            # Re-construct array by pushing comment objects.
            {"$group": {"_id": "$_id", "comments": {"$push": "$comments"}}},
        ]

        for university in self.universities.aggregate(pipeline):
            university['_id'] = str(university['_id'])
            for comment in university["comments"]:
                comment["_id"] = str(comment["_id"])
                data_to_return.append(comment)
        return make_response(jsonify({"total": len(count["comments"]), "comments": data_to_return}), 200)

# Get a single comment

    def show_comment_by_id(self, eid, cid):

        comment = self.universities.find_one(
            {"comments._id": ObjectId(cid)},
            {"_id": 0, "comments.$": 1})
        if comment is None:
            return make_response(
                jsonify(
                    {"error": "Invalid comment ID"}), 404)
        comment['comments'][0]['_id'] = \
            str(comment['comments'][0]['_id'])
        return make_response(jsonify(comment['comments'][0]), 200)

# Update a comment
    @JWTDecorator.jwt_required
    def edit_comment(self, uid, cid):
        try:
            comment = Comment()
            comment.text = request.form["text"]
            comment.uptdTimestamp = datetime.datetime.now()
            comment.isEdited = True
            token = request.headers['x-access-token']
            # Get username from logged in user.
            data = jwt.decode(token, config.config['SECRET_KEY'])
            comment.username = data['user']
            comment.user_id = data['user_id']

            findComment = self.universities.find_one({"comments._id": ObjectId(cid)}, {
                "_id": 0, "comments.$": 1})

            if comment.username == findComment["comments"][0]["username"]:
                self.universities.update_one(
                    {"comments._id": ObjectId(cid)},
                    {"$set": {"comments.$.text": comment.text,
                              "comments.$.uptdTimestamp": comment.uptdTimestamp,
                              "comments.$.isEdited": comment.isEdited}})

                return make_response(jsonify({"message": "Comment updated"}), 200)
            else:
                return make_response(jsonify({"error": "Only the creator can edit a comment."}), 403)
        except KeyError:
            return make_response(jsonify({"error": "One or more fields does not exist."}), 403)

# Delete a comment

    def remove_comment(self, uid, cid):
        self.universities.update_one(
            {"comments.user_id": uid},
            {"$pull": {"comments":
                       {"_id": ObjectId(cid)}}})
        return make_response(jsonify({}), 204)


# Get comments belonging to a user.


    @JWTDecorator.jwt_required
    def show_comment_by_user_id(self, uid):
        comments = []
        for university in self.universities.find():
            university['_id'] = str(university['_id'])
            for comment in university["comments"]:
                comment["_id"] = str(comment["_id"])
            if comment["user_id"] == uid:
                comments.append(comment)
        return make_response(jsonify(comments), 200)
