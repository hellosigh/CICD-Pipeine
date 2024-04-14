from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import path
import logging

from sqlalchemy.sql.functions import user

app = Flask(__name__)

# Define the directory where the SQLite database file will be stored
db_dir = path.abspath(path.dirname(__file__))
db_file = "mydatabase.db"
db_uri = "sqlite:///" + path.join(db_dir, db_file)

# Configure the Flask app to use the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {"id": self.id, "username": self.username, "email": self.email}

# Create the database tables
with app.app_context():
    db.create_all()

# Configure logging level
app.logger.setLevel(logging.DEBUG)

@app.route('/')
def index():
    app.logger.debug('Debug message')
    app.logger.info('Info message')
    app.logger.warning('Warning message')
    app.logger.error('Error message')
    app.logger.critical('Critical message')
    return 'Hello, World!'

# Define API endpoints and error handlers...
@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        app.logger.debug('Received data: %s', data)  # Log received data
        new_user = User(username=data["username"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message": "user created"}), 201)
    except Exception as e:
        app.logger.error('Error creating user: %s', e)  # Log error
        return make_response(jsonify({"message": "error creating user"}), 500)

# Define GET route to get all users
@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except Exception as e:
        app.logger.error('Error getting users: %s', e)  # Log error
        return make_response(jsonify({"message": "error getting users"}), 500)

# get a user by id
@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({"user": user.json()}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"message": "error getting user"}), 500)

    # update a user
    @app.route("/users/<int:id>", methods=["PUT"])
    def update_user(id):
        try:
            user = User.query.filter_by(id=id).first()
            if user:
                data = request.get_json()
                user.username = data["username"]
                user.email = data["email"]
                db.session.commit()
                return make_response(jsonify({"message": "user updated"}), 200)
            return make_response(jsonify({"message": "user not found"}), 404)
        except Exception as e:
            return make_response(jsonify({"message": "error updating user"}), 500)
# delete a user
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message": "user deleted"}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"message": "error deleting user"}), 500)


if __name__ == '__main__':
    app.run(debug=True)
print("SQLite database URI:", db_uri)
