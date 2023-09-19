from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.user_authentication.models import User
from .user_service import register_user,login_user,get_user_profile

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response, status_code = register_user(data)
    return response, status_code


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response, status_code = login_user(data)
    return response, status_code

@user_bp.route('/user/profile', methods=['GET'])
@jwt_required()  # Requires a valid access token for authentication
def get_profile():
    user_data, status_code = get_user_profile()
    return user_data, status_code