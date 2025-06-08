from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.models import User
from . import auth_bp
from auth.models import db

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    # Convert string ID back to integer for database query
    user = User.query.get(int(current_user_id))
    response = jsonify({
        'message': 'This is a protected route',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200
    db.session.close()
    return response