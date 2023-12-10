from models.user import User
from flask import Flask, request, jsonify, make_response, Response
from bson import ObjectId
import datetime
import jwt
import config
from decorators.jwt_decorator import JWTDecorator
import bcrypt
from models.user import User
from models.blacklist import Blacklist


class UserService():

    def __init__(self):
        self.users = User._get_collection()

    @JWTDecorator.jwt_required
    def get_user_details(self, id):

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.config['SECRET_KEY'])

        # Prevent other users from seeing a users bookmarks.
        if data['user_id'] != id:
            return make_response(jsonify({"error": "User ID is invalid"}), 409)

        user = self.users.find_one({'_id': ObjectId(id)})

        if user:
            userDetails = {
                'user_id': str(user['_id']),
                'username': user['username'],
                'email': user['email'],
                'forename': user['forename'],
                'surname': user['surname'],
                'crtdTimestamp': user["crtdTimestamp"],
                'isAdmin': user["isAdmin"]
            }
            return make_response(jsonify([userDetails]), 200)

        else:
            return make_response(jsonify({"error": "The requested resource was not found."}), 404)

    # SignUp

    def signUp(self):
        try:
            newUser = User()
            newUser.username = request.json["username"]
            newUser.email = request.json["email"]
            newUser.forename = request.json["forename"]
            newUser.surname = request.json["surname"]
            newUser.password = request.json["password"]
            newUser.crtdTimestamp = datetime.datetime.utcnow()
            # Check if username or password exists
            if self.users.find_one({'username': newUser.username}) == None\
                    and self.users.find_one({'email': newUser.email}) == None:
                newUser.password = bcrypt.hashpw(
                    newUser.password.encode('utf8'), bcrypt.gensalt())
                newUser.save()
                return make_response(jsonify({"message": "User created."}), 201)

            return make_response(jsonify({"message": "Username or email already exists."}), 409)
        except KeyError:
            return make_response(jsonify({"message": "One or more fields are missing or invalid."}), 403)
# Login

    def login(self):
        auth = request.authorization

        if auth:
            user = self.users.find_one({'username': auth.username})
            if user is not None:
                if bcrypt.checkpw(bytes(auth.password, 'UTF-8'),
                                  user["password"]):
                    token = jwt.encode(
                        {'user': auth.username,
                         # Encode userID into jwt
                         'user_id':  str(user['_id']),
                         'isAdmin': user["isAdmin"],
                         'exp': datetime.datetime.utcnow() +
                         datetime.timedelta(minutes=30)
                         }, config.config['SECRET_KEY'])
                    return make_response(jsonify(
                        {'token': token.decode('UTF-8'), 'url': 'http://127.0.0.1:5000/api/v1.0/users/' + str(user['_id'])}), 200)
                else:
                    return make_response(jsonify(
                        {'message': 'Bad password'}), 401)
            else:
                return make_response(jsonify(
                    {'message': 'Bad username'}), 401)
        return make_response(jsonify(
            {'message': 'Authentication required'}), 401)

    # Logout

    # @JWTDecorator.jwt_required
    def logout(self):
        blacklist = Blacklist._get_collection()
        token = request.headers['x-access-token']
        blacklist.insert_one({"token": token})
        return make_response(jsonify({'message': 'Logout successful'}), 200)
