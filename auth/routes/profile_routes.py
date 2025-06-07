from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.models import db, User
from . import auth_bp

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update only the fields that are provided
    if 'name' in data:
        user.name = data['name']
    if 'avatarUrl' in data:
        user.avatarUrl = data['avatarUrl']
    if 'bio' in data:
        user.bio = data['bio']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'avatarUrl': user.avatarUrl,
                'bio': user.bio,
                'createdAt': user.createdAt.isoformat()
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'avatarUrl': user.avatarUrl,
        'bio': user.bio,
        'createdAt': user.createdAt.isoformat()
    }), 200 