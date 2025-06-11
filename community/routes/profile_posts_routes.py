from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from community.models import Post, db
from . import community_bp

@community_bp.route('/profile/posts', methods=['POST'])
@jwt_required()
def create_profile_post():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400
    
    try:
        new_post = Post(
            title=data['title'],
            content=data['content'],
            author_id=int(current_user_id),
            post_type='profile'
        )
        
        db.session.add(new_post)
        db.session.commit()
        
        return jsonify({
            'message': 'Post created successfully',
            'post': new_post.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()

@community_bp.route('/profile/<int:user_id>/posts', methods=['GET'])
@jwt_required()
def get_user_posts(user_id):
    try:
        posts = Post.query.filter_by(author_id=user_id, post_type='profile').order_by(Post.created_at.desc()).all()
        posts_data = []
        for post in posts:
            post_dict = post.to_dict()
            post_dict['author'] = post.author.to_dict() if post.author else None
            posts_data.append(post_dict)
        return jsonify({
            'posts': posts_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()

@community_bp.route('/profile/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_profile_post(post_id):
    current_user_id = get_jwt_identity()
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    if post.author_id != int(current_user_id):
        return jsonify({'error': 'Unauthorized to update this post'}), 403
    
    if post.post_type != 'profile':
        return jsonify({'error': 'This is not a profile post'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        
        db.session.commit()
        return jsonify({
            'message': 'Post updated successfully',
            'post': post.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()

@community_bp.route('/profile/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_profile_post(post_id):
    current_user_id = get_jwt_identity()
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    if post.author_id != int(current_user_id):
        return jsonify({'error': 'Unauthorized to delete this post'}), 403
    
    if post.post_type != 'profile':
        return jsonify({'error': 'This is not a profile post'}), 400
    
    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close() 