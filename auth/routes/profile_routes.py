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

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query users with pagination
        paginated_users = User.query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Prepare response
        users_data = [user.to_dict() for user in paginated_users.items]
        
        return jsonify({
            'users': users_data,
            'total': paginated_users.total,
            'pages': paginated_users.pages,
            'current_page': page,
            'has_next': paginated_users.has_next,
            'has_prev': paginated_users.has_prev
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close() 