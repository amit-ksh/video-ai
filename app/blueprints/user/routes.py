from flask import request, Blueprint, jsonify

from app.blueprints.user.models import User

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        return {"message": "Email and password are required"}, 400

    if User.get_user_by_email(email):
        return {"message": "User already exists"}, 400

    return User.create_user(email, password).to_json()


@user_bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user = User.validate_user(email, password)
    if user:
        return jsonify(access_token=user.generate_access_token()), 200
    else:
        return "Invalid credentials", 400
