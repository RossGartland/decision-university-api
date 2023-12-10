from models.university import University
from flask import Flask, request, jsonify, make_response, Response
from bson import ObjectId
from models.comments import Comment
import datetime
from decorators.jwt_decorator import JWTDecorator
import jwt
import config
# Comments


class ReactionService():
    # Add a comment

    def __init__(self):
        self.universities = University._get_collection()

    # Add a like reaction
    @JWTDecorator.jwt_required
    def add_reaction(self, eid, cid):
        comment = Comment()
        reactionType = request.json["reactionType"]
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.config['SECRET_KEY'])
        comment.username = data['user']

        likeReactions = self.universities.find_one(
            {"comments._id": ObjectId(cid)},
            {"comments.likeReactions.$": 1})

        angryReactions = self.universities.find_one(
            {"comments._id": ObjectId(cid)},
            {"comments.angryReactions.$": 1})

        laughReactions = self.universities.find_one(
            {"comments._id": ObjectId(cid)},
            {"comments.laughReactions.$": 1})

        if comment.username in likeReactions["comments"][0]["likeReactions"] \
            or comment.username in angryReactions["comments"][0]["angryReactions"] \
                or comment.username in laughReactions["comments"][0]["laughReactions"]:
            return make_response(jsonify("Only 1 reaction allowed."), 405)

        if reactionType == "likeReaction":
            self.universities.update_one(
                {"comments._id": ObjectId(cid)},
                {"$addToSet": {"comments.$.likeReactions": comment.username}})
            return make_response(jsonify({"message": "Like reaction added."}), 201)
        elif reactionType == "laughReaction":
            self.universities.update_one(
                {"comments._id": ObjectId(cid)},
                {"$addToSet": {"comments.$.laughReactions": comment.username}})
            return make_response(jsonify({"message": "Laugh reaction added."}), 201)
        elif reactionType == "angryReaction":
            self.universities.update_one(
                {"comments._id": ObjectId(cid)},
                {"$addToSet": {"comments.$.angryReactions": comment.username}})
            return make_response(jsonify({"message": "Angry reaction added."}), 201)
        else:
            return make_response(jsonify({"message": "Reaction already sent."}), 200)

    # Get like reactions
    def get_react_count(self, eid, cid):
        try:
            likeReactions = self.universities.find_one(
                {"comments._id": ObjectId(cid)},
                {"comments.likeReactions.$": 1})
            laughReactions = self.universities.find_one(
                {"comments._id": ObjectId(cid)},
                {"comments.laughReactions.$": 1})
            angryReactions = self.universities.find_one(
                {"comments._id": ObjectId(cid)},
                {"comments.angryReactions.$": 1})

            reactionsCount = {
                "likeReactions": len(likeReactions["comments"][0]["likeReactions"]),
                "laughReactions": len(laughReactions["comments"][0]["laughReactions"]),
                "angryReactions": len(angryReactions["comments"][0]["angryReactions"])
            }
            return make_response(jsonify(reactionsCount), 200)
        except:
            return make_response(jsonify({"message": "No like reactions found"}), 204)

    # Delete reaction
    @JWTDecorator.jwt_required
    def remove_reaction(self, eid, cid):
        comment = Comment()
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.config['SECRET_KEY'])
        comment.username = data['user']

        likeReactions = self.universities.find_one(
            {"comments._id": ObjectId(cid)},
            {"comments.likeReactions.$": 1})
        if comment.username in likeReactions["comments"][0]["likeReactions"]:
            self.universities.update_one(
                {"comments._id": ObjectId(cid)},
                {"$pull": {"comments.$.likeReactions": comment.username}})
            return make_response(jsonify({"message": "Like removed"}), 204)

        angryReactions = self.universities.find_one(
            {"comments._id": ObjectId(cid)},
            {"comments.angryReactions.$": 1})
        if comment.username in angryReactions["comments"][0]["angryReactions"]:
            self.universities.update_one(
                {"comments._id": ObjectId(cid)},
                {"$pull": {"comments.$.angryReactions": comment.username}})
            return make_response(jsonify({"message": "Angry react removed"}), 204)

        laughReactions = self.universities.find_one(
            {"comments._id": ObjectId(cid)},
            {"comments.laughReactions.$": 1})
        if comment.username in laughReactions["comments"][0]["laughReactions"]:
            self.universities.update_one(
                {"comments._id": ObjectId(cid)},
                {"$pull": {"comments.$.laughReactions": comment.username}})
            return make_response(jsonify({"message": "Laugh react removed"}), 204)
        return make_response(jsonify({"message": "No reactions found"}), 204)
