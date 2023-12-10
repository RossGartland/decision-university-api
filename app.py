from database_connection import DatabaseConnection
from flask import Flask
from controllers.university_controller import university_blueprint
from controllers.comments_controller import comments_blueprint
from controllers.user_controller import user_blueprint
from controllers.reaction_controller import reactions_blueprint
from controllers.bookmark_controller import bookmark_blueprint
import jwt
import datetime
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(university_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(comments_blueprint)
app.register_blueprint(reactions_blueprint)
app.register_blueprint(bookmark_blueprint)
app.wsgi_app = DatabaseConnection(app.wsgi_app)
CORS(app)


if __name__ == "__main__":
    app.run(debug=True)
