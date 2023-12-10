from flask import Flask, request, jsonify, make_response, Blueprint
from services.user_service import UserService

# Route controller with app.
user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route("/api/v1.0/users/<string:id>", methods=["GET"])
def get_user_details(id):
    return UserService().get_user_details(id)


@user_blueprint.route("/api/v1.0/signup", methods=["POST"])
def signUp():
    return UserService().signUp()


@user_blueprint.route("/api/v1.0/login", methods=["GET"])
def login():
    return UserService().login()


@user_blueprint.route("/api/v1.0/logout", methods=["GET"])
def logout():
    return UserService().logout()
