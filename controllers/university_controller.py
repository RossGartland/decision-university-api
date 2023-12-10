from flask import Flask, request, jsonify, make_response, Blueprint
from services.university_service import UniversityService

# Route controller with app.
university_blueprint = Blueprint('university_blueprint', __name__)


@university_blueprint.route("/api/v1.0/universities", methods=["GET"])
def get_universities():
    return UniversityService().get_universities()


@university_blueprint.route("/api/v1.0/universities/count", methods=["GET"])
def get_university_count():
    return UniversityService().get_university_count()


@university_blueprint.route("/api/v1.0/universities", methods=["POST"])
def create__university():
    return UniversityService().add_university()


@university_blueprint.route("/api/v1.0/universities/<string:id>", methods=["GET"])
def find_university_by_id(id):
    return UniversityService().get_university_by_id(id)


@university_blueprint.route("/api/v1.0/universities/<string:id>", methods=["PUT"])
def update_an_university(id):
    return UniversityService().update_university(id)


@university_blueprint.route("/api/v1.0/universities/<string:id>", methods=["DELETE"])
def delete_an_university(id):
    return UniversityService().delete_university(id)


@university_blueprint.route("/api/v1.0/universities/search", methods=["GET"])
def search_by_institution():
    return UniversityService().search_by_institution()
