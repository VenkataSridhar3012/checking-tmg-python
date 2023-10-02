from flask import jsonify
from .user_models import db, User
from app.user_config.user_config_model import UserConfig , user_config_to_json
from flask_jwt_extended import create_access_token, get_jwt_identity
import bcrypt
from datetime import timedelta


def register_user(data):
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid request'}), 400

    email = data['email']
    password = data['password']

    # Check if the username already exists in the database
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    # Hash the user's password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user and add it to the database with the hashed password
    new_user = User(email=email, password=hashed_password.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    
    # Create a configuration and associate it with the user
    config = UserConfig(user_id=new_user.id)
    db.session.add(config)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

def login_user(data):
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid request'}), 400

    email = data['email']
    password = data['password']

    # Check if the user exists in the database
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # The entered password matches the stored hashed password
        # Create a custom dictionary of data to include in the token
        
        # Generate an access token for the user
        access_token = create_access_token(identity={'userid': user.id, 'email': user.email})
        # find user config details
        user_config = UserConfig.query.filter_by(user_id=user.id).first()
        user_config_json = user_config_to_json(user_config)
        # Return the token in the response JSON
        return jsonify({'message': 'Login successful', 'access_token': access_token,'user_config':user_config_json}), 200
    else:
        return jsonify({'message': 'Login failed'}), 401
       
def get_user_profile():
    # Get the current user's identity from the JWT token
    current_user =get_jwt_identity()
    # Access the claims directly from the identity
    userid = current_user.get('jwt', {}).get('userid')
    email = current_user.get('jwt', {}).get('email')
    
    print(userid,email)
    # Fetch user data from your database based on the username
    user = User.query.filter_by(email=current_user['email']).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Serialize the user data as needed
    user_data = {
        'email': user.email,
        # Add more user attributes as needed
    }

    return user_data, 200    