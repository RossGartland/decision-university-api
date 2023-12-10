from flask import Flask, request, jsonify, make_response, Blueprint
from services.comment_service import CommentService
from services.reaction_service import ReactionService

# Route controller with app.
comments_blueprint = Blueprint('comments_blueprint', __name__)


@comments_blueprint.route("/api/v1.0/universities/<string:id>/comments", methods=["Post"])
def add_a_new_comment(id):
    return CommentService().add_new_comment(id)


@comments_blueprint.route("/api/v1.0/universities/<string:id>/comments", methods=["GET"])
def get_all_commentst(id):
    return CommentService().show_all_comments(id)


@comments_blueprint.route("/api/v1.0/universities/<string:eid>/comments/<string:cid>", methods=["GET"])
def get_comment_by_id(eid, cid):
    return CommentService().show_comment_by_id(eid, cid)


@comments_blueprint.route("/api/v1.0/users/<string:uid>/comments/<string:cid>", methods=["PUT"])
def update_comment(uid, cid):
    return CommentService().edit_comment(uid, cid)


@comments_blueprint.route("/api/v1.0/users/<string:uid>/comments/<string:cid>", methods=["DELETE"])
def delete_comment(uid, cid):
    return CommentService().remove_comment(uid, cid)


@comments_blueprint.route("/api/v1.0/users/<string:uid>/comments", methods=["GET"])
def get_comment_by_user_id(uid):
    return CommentService().show_comment_by_user_id(uid)
