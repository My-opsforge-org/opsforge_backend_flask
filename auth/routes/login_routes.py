from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from auth.models import User
from . import auth_bp

bcrypt = Bcrypt()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data['username']  # This can be username or email
    password = data['password']

    # Check if identifier is an email
    if '@' in identifier:
        user = User.query.filter_by(email=identifier).first()
    else:
        user = User.query.filter_by(username=identifier).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        # Convert user.id to string for JWT token
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'message': 'Login successful'
        }), 200
    
    return jsonify({'error': 'Invalid username/email or password'}), 401 