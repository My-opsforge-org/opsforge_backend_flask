from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from auth.models import User
from community.models import Post, Reaction

reaction_bp = Blueprint('reaction', __name__)

@reaction_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    existing_reaction = Reaction.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()
    
    if existing_reaction:
        if existing_reaction.reaction_type == 'like':
            return jsonify({'message': 'Post already liked'}), 200
        existing_reaction.reaction_type = 'like'
    else:
        reaction = Reaction(
            user_id=user_id,
            post_id=post_id,
            reaction_type='like'
        )
        db.session.add(reaction)
    
    db.session.commit()
    return jsonify({'message': 'Post liked successfully'}), 200

@reaction_bp.route('/posts/<int:post_id>/dislike', methods=['POST'])
@jwt_required()
def dislike_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    existing_reaction = Reaction.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()
    
    if existing_reaction:
        if existing_reaction.reaction_type == 'dislike':
            return jsonify({'message': 'Post already disliked'}), 200
        existing_reaction.reaction_type = 'dislike'
    else:
        reaction = Reaction(
            user_id=user_id,
            post_id=post_id,
            reaction_type='dislike'
        )
        db.session.add(reaction)
    
    db.session.commit()
    return jsonify({'message': 'Post disliked successfully'}), 200

@reaction_bp.route('/posts/<int:post_id>/reaction', methods=['DELETE'])
@jwt_required()
def remove_reaction(post_id):
    user_id = get_jwt_identity()
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    reaction = Reaction.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first_or_404()
    
    db.session.delete(reaction)
    db.session.commit()
    return jsonify({'message': 'Reaction removed successfully'}), 200 