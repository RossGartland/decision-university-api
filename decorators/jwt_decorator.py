from database_connection import DatabaseConnection
from flask import Flask, request, jsonify, make_response
import jwt
import datetime
from functools import wraps
from models.user import User
import config
from models.blacklist import Blacklist


class JWTDecorator():
    def __init__(self):
        self.users = User._get_collection()
        self.blacklist = Blacklist._get_collection()

    def jwt_required(func):
        @wraps(func)
        def jwt_required_wrapper(*args, **kwargs):
            token = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token:
                return jsonify(
                    {'message': 'Token is missing'}), 401
            try:
                data = jwt.decode(token,
                                  config.config['SECRET_KEY'])
            except:
                return jsonify(
                    {'message': 'Token is invalid'}), 401
            blacklist = Blacklist._get_collection()
            bl_token = blacklist.find_one({"token": token})
            if bl_token is not None:
                return make_response(jsonify({'message': 'Token has been cancelled'}), 401)
            return func(*args, **kwargs)
        return jwt_required_wrapper

    def admin_required(func):
        @wraps(func)
        def admin_required_wrapper(*args, **kwargs):
            token = request.headers['x-access-token']
            data = jwt.decode(token,
                              config.config['SECRET_KEY'])
            if data["isAdmin"]:
                return func(*args, **kwargs)
            else:
                return make_response(jsonify({'message': 'Admin access required'}), 401)
        return admin_required_wrapper
