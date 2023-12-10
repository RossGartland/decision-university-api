from pymongo import MongoClient
import mongoengine
from flask import Flask, request, jsonify, make_response
# Connection class for MongoDB Collection.


class DatabaseConnection:
    def __init__(self, app):
        self.__app = app

    def __call__(self, environ, start_response):
        try:
            mongoengine.connect(db="com661",
                                   host="mongodb://127.0.0.1:27017")  # Connection to mongo database.

            return self.__app(environ, start_response)
        except ConnectionError as e:
            res = make_response(u'Connection to mongo failed',
                                mimetype='application/json', status=501)
            return res(environ, start_response)
