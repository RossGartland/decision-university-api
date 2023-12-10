from models.university import University
from flask import request, jsonify, make_response
from bson import ObjectId
from models.comments import Comment
import datetime
from decorators.jwt_decorator import JWTDecorator
from mongoengine.errors import ValidationError
import pymongo


class UniversityService():

    def __init__(self):
        self.universities = University._get_collection()

    # Get all universities and sort via university rank.
    def get_universities(self):

        page_num, page_size, sort = 1, 10, pymongo.ASCENDING
        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))
        if request.args.get('sort') == "rankdesc":  # Get sorting criteria
            sort = pymongo.DESCENDING
        elif request.args.get('sort') == "rankasc":
            sort = pymongo.ASCENDING
        page_start = (page_size * (page_num - 1))

        pipeline = [
            {"$sort": {"r2022": sort}},
            {"$skip": page_start},
            {"$limit": page_size},
        ]
        universities = []
        for university in self.universities.aggregate(pipeline):
            university['_id'] = str(university['_id'])
            for comment in university['comments']:
                comment['_id'] = str(comment['_id'])
            universities.append(university)

        return make_response(jsonify(universities), 200)

    # Get total number of universities
    def get_university_count(self):
        count = self.universities.count_documents({})
        return make_response(jsonify(count), 200)

# Get university by id
    def get_university_by_id(self, id):

        university = self.universities.find_one({'_id': ObjectId(id)})

        if university:
            university['_id'] = str(university['_id'])
            for comment in university['comments']:
                comment['_id'] = str(comment['_id'])
            return make_response(jsonify([university]), 200)

        else:
            return make_response(jsonify({"error": "The requested resource was not found."}), 404)

# Create a new university
    @JWTDecorator.jwt_required
    @JWTDecorator.admin_required
    def add_university(self):
        try:
            university = University()
            university.r2022 = request.json["r2022"]
            university.r2021 = request.json["r2021"]
            university.score = request.json["score"]
            university.course = request.json["course"]
            university.teaching = request.json["teaching"]
            university.feedback = request.json["feedback"]
            university.ratio = request.json["ratio"]
            university.spend = request.json["spend"]
            university.tariff = request.json["tariff"]
            university.career = request.json["career"]
            university.continuation = request.json["continuation"]
            university.institution = request.json["institution"]
            university.comments = []
            university.crtdTimestamp = datetime.datetime.utcnow()
            university.save()

            return make_response(jsonify({"message": "university added.",
                                          "url": "http://127.0.0.1:5000/api/v1.0/universities/"+str(university.id)}), 201)
        except ValidationError:
            return make_response(jsonify({"error": "One or more fields contains invalid data."}), 403)


# Update a university

    @JWTDecorator.jwt_required
    @JWTDecorator.admin_required
    def update_university(self, id):
        try:
            university = self.universities.find_one({'_id': ObjectId(id)})

            university = University()
            university.r2022 = request.json["r2022"]
            university.r2021 = request.json["r2021"]
            university.score = request.json["score"]
            university.course = request.json["course"]
            university.teaching = request.json["teaching"]
            university.feedback = request.json["feedback"]
            university.ratio = request.json["ratio"]
            university.spend = request.json["spend"]
            university.tariff = request.json["tariff"]
            university.career = request.json["career"]
            university.continuation = request.json["continuation"]
            university.institution = request.json["institution"]
            university.uptdTimestamp = datetime.datetime.utcnow()

            if university is not None:
                self.universities.update_one(
                    {"_id": ObjectId(id)}, {
                        "$set": {"r2022": university.r2022,
                                 "r2021": university.r2021,
                                 "score": university.score,
                                 "course": university.course,
                                 "teaching": university.teaching,
                                 "feedback": university.feedback,
                                 "ratio": university.ratio,
                                 "spend": university.spend,
                                 "tariff": university.tariff,
                                 "career": university.career,
                                 "continuation": university.continuation,
                                 "institution": university.institution,
                                 "uptdTimestamp": university.uptdTimestamp
                                 }
                    })
                return make_response(jsonify("Updated"), 200)
            else:
                return make_response(jsonify({"error": "The requested resource was not found."}), 404)
        except KeyError:
            return make_response(jsonify({"error": "One or more fields does not exist."}), 403)

# Delete a university
    @JWTDecorator.jwt_required
    @JWTDecorator.admin_required
    def delete_university(self, id):
        university = self.universities.delete_one({'_id': ObjectId(id)})
        if university.deleted_count == 1:
            return make_response(jsonify({}), 204)
        else:
            return make_response(jsonify({"error": "Invalid business ID"}), 404)

# Search by university name
    def search_by_institution(self):
        page_num, page_size = 1, 10
        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))
        page_start = (page_size * (page_num - 1))
        if request.args.get('institution'):
            institution = str(request.args.get('institution'))
            universities = []
            for university in self.universities.find({'$text': {'$search': institution}}) \
                    .skip(page_start).limit(page_size):
                university['_id'] = str(university['_id'])
                for comment in university['comments']:
                    comment['_id'] = str(comment['_id'])
                universities.append(university)
            if len(universities) > 0:
                return make_response(jsonify(universities), 200)
            return make_response("Sorry, there are no results matching your search.", 404)
        return make_response("You must enter valid search criteria.", 405)
