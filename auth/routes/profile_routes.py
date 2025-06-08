from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.models import db, User
from . import auth_bp

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if not user:
        db.session.close()
        return jsonify({'error': 'User not found'}), 404

    response = jsonify(user.to_dict()), 200
    db.session.close()
    return response

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if not user:
        db.session.close()
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        db.session.close()
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        user.update_from_dict(data)
        db.session.commit()
        response = jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        db.session.close()
        return response
    except ValueError as e:
        db.session.rollback()
        db.session.close()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        db.session.close()
        return jsonify({'error': 'Failed to update profile'}), 500 