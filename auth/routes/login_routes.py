from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from auth.models import User
from . import auth_bp

bcrypt = Bcrypt()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        # Convert user.id to string for JWT token
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'message': 'Login successful'
        }), 200
    
    return jsonify({'error': 'Invalid username or password'}), 401 