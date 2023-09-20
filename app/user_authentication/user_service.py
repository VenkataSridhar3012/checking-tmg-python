from flask import jsonify
from .user_models import db, User
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
import bcrypt

def register_user(data):
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid request'}), 400

    username = data['username']
    userId = data['userId']
    password = data['password']

    # Check if the username already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    # Hash the user's password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user and add it to the database with the hashed password
    new_user = User(username=username, password=hashed_password.decode('utf-8'),userId=userId)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

def login_user(data):
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid request'}), 400

    username = data['username']
    password = data['password']

    # Check if the user exists in the database
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # The entered password matches the stored hashed password
        # Generate an access token for the user
        access_token = create_access_token(identity=username)

        # Return the token in the response JSON
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Login failed'}), 401
       
def get_user_profile():
    # Get the current user's identity from the JWT token
    current_user = get_jwt_identity()

    # Fetch user data from your database based on the username
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Serialize the user data as needed
    user_data = {
        'username': user.username,
        'email': user.email,
        # Add more user attributes as needed
    }

    return user_data, 200    