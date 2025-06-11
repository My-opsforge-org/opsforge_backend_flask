from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.models import User, db
from . import auth_bp

@auth_bp.route('/users/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    user_to_follow = User.query.get_or_404(user_id)
    
    if current_user_id == user_id:
        return jsonify({'error': 'You cannot follow yourself'}), 400
    
    if current_user.follow(user_to_follow):
        db.session.commit()
        return jsonify({'message': f'Successfully followed {user_to_follow.name}'}), 200
    return jsonify({'message': f'Already following {user_to_follow.name}'}), 200

@auth_bp.route('/users/<int:user_id>/unfollow', methods=['POST'])
@jwt_required()
def unfollow_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    user_to_unfollow = User.query.get_or_404(user_id)
    
    if current_user.unfollow(user_to_unfollow):
        db.session.commit()
        return jsonify({'message': f'Successfully unfollowed {user_to_unfollow.name}'}), 200
    return jsonify({'message': f'Not following {user_to_unfollow.name}'}), 200

@auth_bp.route('/users/<int:user_id>/followers', methods=['GET'])
@jwt_required()
def get_followers(user_id):
    user = User.query.get_or_404(user_id)
    followers = [follower.to_dict() for follower in user.followers]
    return jsonify({'followers': followers}), 200

@auth_bp.route('/users/<int:user_id>/following', methods=['GET'])
@jwt_required()
def get_following(user_id):
    user = User.query.get_or_404(user_id)
    following = [followed.to_dict() for followed in user.following]
    return jsonify({'following': following}), 200 