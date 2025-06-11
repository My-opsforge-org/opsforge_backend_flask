from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from auth.models import User
from community.models import Post, Comment

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'Comment content is required'}), 400
    
    post = Post.query.get_or_404(post_id)
    comment = Comment(
        content=content,
        author_id=user_id,
        post_id=post_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify(comment.to_dict()), 201

@comment_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@jwt_required()
def get_post_comments(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
    return jsonify([comment.to_dict() for comment in comments]), 200

@comment_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.get_or_404(comment_id)
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    if comment.author_id != user_id:
        return jsonify({
            'error': 'You can only edit your own comments',
            'details': {
                'user_id': user_id,
                'comment_author_id': comment.author_id,
                'comment_id': comment_id
            }
        }), 403
    
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'Comment content is required'}), 400
    
    comment.content = content
    db.session.commit()
    
    return jsonify(comment.to_dict()), 200

@comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.get_or_404(comment_id)
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    if comment.author_id != user_id:
        return jsonify({
            'error': 'You can only delete your own comments',
            'details': {
                'user_id': user_id,
                'comment_author_id': comment.author_id,
                'comment_id': comment_id
            }
        }), 403
    
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment deleted successfully'}), 200 