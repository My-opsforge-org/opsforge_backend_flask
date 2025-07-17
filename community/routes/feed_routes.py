from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.models import User
from community.models import Post, Community, db
from . import community_bp

@community_bp.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    
    # Get page and per_page parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    try:
        # Get community IDs
        community_ids = [c.id for c in current_user.communities_joined]
        # Get followed user IDs
        followed_user_ids = [u.id for u in current_user.following]
        # Ensure current user's own posts are included
        if current_user_id not in followed_user_ids:
            followed_user_ids.append(current_user_id)
        
        # Base query for posts
        query = Post.query
        posts = []

        # If user has communities or follows users, filter by them
        if community_ids or followed_user_ids:
            conditions = []
            if community_ids:
                conditions.append(Post.community_id.in_(community_ids))
            if followed_user_ids:
                conditions.append(Post.author_id.in_(followed_user_ids))
            filtered_query = query.filter(db.or_(*conditions))
            posts += filtered_query.all()
        # Always include the user's own profile posts
        profile_posts = Post.query.filter_by(author_id=current_user_id, post_type='profile').all()
        posts += profile_posts
        # Remove duplicates by post id
        unique_posts = {post.id: post for post in posts}.values()
        # Sort by created_at descending
        sorted_posts = sorted(unique_posts, key=lambda p: p.created_at, reverse=True)
        # Paginate manually
        total = len(sorted_posts)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_posts = sorted_posts[start:end]
        # Prepare the response
        posts_data = []
        for post in paginated_posts:
            post_dict = post.to_dict()
            post_dict['author'] = post.author.to_dict() if post.author else None
            if post.community_id:
                post_dict['community'] = post.community.to_dict()
            posts_data.append(post_dict)
        return jsonify({
            'posts': posts_data,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'current_page': page,
            'has_next': end < total,
            'has_prev': start > 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close() 