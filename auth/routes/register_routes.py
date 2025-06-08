from flask import request, jsonify
from flask_bcrypt import Bcrypt
from auth.models import User
from . import auth_bp
from app import db

bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate username (no @ allowed)
    if '@' in data['username']:
        return jsonify({
            'error': 'Username cannot contain @ symbol'
        }), 400
    
    # Validate email (must contain @)
    if '@' not in data['email']:
        return jsonify({
            'error': 'Invalid email format'
        }), 400
    
    # Check if user already exists
    try:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'User created successfully'}), 201
    finally:
        db.session.close()