from flask import Flask, request, jsonify, make_response, Blueprint
from services.bookmark_service import BookmarkService
from services.reaction_service import ReactionService

# Route controller with app.
bookmark_blueprint = Blueprint('bookmark_blueprint', __name__)


@bookmark_blueprint.route("/api/v1.0/users/<string:id>/bookmarks", methods=["Post"])
def add_new_bookmark(id):
    return BookmarkService().add_new_bookmark(id)


@bookmark_blueprint.route("/api/v1.0/users/<string:id>/bookmarks", methods=["GET"])
def show_all_bookmarks_for_user(id):
    return BookmarkService().show_all_bookmarks_for_user(id)


@bookmark_blueprint.route("/api/v1.0/users/<string:uid>/bookmarks/<string:bid>", methods=["GET"])
def show_bookmark_by_id(uid, bid):
    return BookmarkService().show_bookmark_by_id(uid, bid)


@bookmark_blueprint.route("/api/v1.0/users/<string:uid>/bookmarks/institution/<string:iid>", methods=["GET"])
def show_bookmark_by_institution_id(uid, iid):
    return BookmarkService().show_bookmark_by_institution_id(uid, iid)


@bookmark_blueprint.route("/api/v1.0/users/<string:uid>/bookmarks/<string:iid>", methods=["DELETE"])
def remove_bookmark(uid, iid):
    return BookmarkService().remove_bookmark(uid, iid)
