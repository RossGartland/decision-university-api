from flask import Flask, request, jsonify, make_response, Blueprint
from services.reaction_service import ReactionService

# Route controller with app.
reactions_blueprint = Blueprint('reactions_blueprint', __name__)


@reactions_blueprint.route("/api/v1.0/universities/<string:eid>/comments/<string:cid>/reactions", methods=["POST"])
def add_reaction(eid, cid):
    return ReactionService().add_reaction(eid, cid)


@reactions_blueprint.route("/api/v1.0/universities/<string:eid>/comments/<string:cid>/reactions", methods=["GET"])
def get_react_count(eid, cid):
    return ReactionService().get_react_count(eid, cid)


@reactions_blueprint.route("/api/v1.0/universities/<string:eid>/comments/<string:cid>/reactions", methods=["DELETE"])
def remove_reaction(eid, cid):
    return ReactionService().remove_reaction(eid, cid)
