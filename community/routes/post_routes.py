from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from auth.models import User
from community.models import Community, Post, Image

post_bp = Blueprint('post', __name__)

@post_bp.route('/communities/<int:community_id>/posts', methods=['POST'])
@jwt_required()
def create_post(community_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    community = Community.query.get_or_404(community_id)
    
    # Get detailed membership information
    member_ids = [member.id for member in community.members]
    is_member = community.is_member(user_id)
    
    if not is_member:
        return jsonify({
            'error': 'You must be a member to create posts',
            'details': {
                'user_id': user_id,
                'community_id': community_id, 
                'member_ids': member_ids,
                'is_member': is_member
            }
        }), 403
    
    title = data.get('title')
    content = data.get('content')
    image_urls = data.get('image_urls', [])
    
    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400
    
    # Validate image_urls is a list
    if not isinstance(image_urls, list):
        return jsonify({'error': 'image_urls must be a list'}), 400
    
    try:
        post = Post(
            title=title,
            content=content,
            author_id=user_id,
            community_id=community_id,
            post_type='community'
        )
        
        # Add images
        for url in image_urls:
            image = Image(url=url, post=post)
            db.session.add(image)
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify(post.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@post_bp.route('/communities/<int:community_id>/posts', methods=['GET'])
@jwt_required()
def get_community_posts(community_id):
    community = Community.query.get_or_404(community_id)
    posts = Post.query.filter_by(community_id=community_id).order_by(Post.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

@post_bp.route('/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    post_dict = post.to_dict(include_comments=True)
    post_dict['author'] = post.author.to_dict() if post.author else None
    return jsonify(post_dict), 200

@post_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    if post.author_id != user_id:
        return jsonify({
            'error': 'You can only edit your own posts',
            'details': {
                'user_id': user_id,
                'post_author_id': post.author_id,
                'post_id': post_id
            }
        }), 403
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    image_urls = data.get('image_urls')
    
    try:
        if title:
            post.title = title
        if content:
            post.content = content
        if image_urls is not None:
            if not isinstance(image_urls, list):
                return jsonify({'error': 'image_urls must be a list'}), 400
            
            # Remove existing images
            for image in post.images:
                db.session.delete(image)
            
            # Add new images
            for url in image_urls:
                image = Image(url=url, post=post)
                db.session.add(image)
        
        db.session.commit()
        return jsonify(post.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@post_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    if post.author_id != user_id:
        return jsonify({
            'error': 'You can only delete your own posts',
            'details': {
                'user_id': user_id,
                'post_author_id': post.author_id,
                'post_id': post_id
            }
        }), 403
    
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200 