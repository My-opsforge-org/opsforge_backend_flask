from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from auth.models import User
from . import auth_bp
from app import db  # Import db instance

bcrypt = Bcrypt()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    try:
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            # Convert user.id to string for JWT token
            access_token = create_access_token(identity=str(user.id))
            return jsonify({
                'access_token': access_token,
                'message': 'Login successful'
            }), 200
        
        return jsonify({'error': 'Invalid email or password'}), 401
    finally:
        db.session.close()  # Ensure session is closed