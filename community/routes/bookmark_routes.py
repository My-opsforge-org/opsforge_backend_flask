from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from auth.models import User
from community.models import Post, Bookmark

bookmark_bp = Blueprint('bookmark', __name__)

@bookmark_bp.route('/posts/<int:post_id>/bookmark', methods=['POST'])
@jwt_required()
def bookmark_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    existing_bookmark = Bookmark.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()
    
    if existing_bookmark:
        return jsonify({'message': 'Post already bookmarked'}), 200
    
    bookmark = Bookmark(
        user_id=user_id,
        post_id=post_id
    )
    
    db.session.add(bookmark)
    db.session.commit()
    
    return jsonify({'message': 'Post bookmarked successfully'}), 200

@bookmark_bp.route('/posts/<int:post_id>/bookmark', methods=['DELETE'])
@jwt_required()
def remove_bookmark(post_id):
    user_id = get_jwt_identity()
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    bookmark = Bookmark.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first_or_404()
    
    db.session.delete(bookmark)
    db.session.commit()
    
    return jsonify({'message': 'Bookmark removed successfully'}), 200

@bookmark_bp.route('/bookmarks', methods=['GET'])
@jwt_required()
def get_bookmarked_posts():
    user_id = get_jwt_identity()
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
    return jsonify([bookmark.post.to_dict() for bookmark in bookmarks]), 200 