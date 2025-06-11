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
        
        # Base query for posts
        query = Post.query
        
        # If user has communities or follows users, filter by them
        if community_ids or followed_user_ids:
            conditions = []
            if community_ids:
                conditions.append(Post.community_id.in_(community_ids))
            if followed_user_ids:
                conditions.append(Post.author_id.in_(followed_user_ids))
            query = query.filter(db.or_(*conditions))
        else:
            # If user has no communities and follows no one, return empty result
            return jsonify({
                'posts': [],
                'total': 0,
                'pages': 0,
                'current_page': page,
                'has_next': False,
                'has_prev': False
            }), 200
        
        # Order by creation date
        query = query.order_by(Post.created_at.desc())
        
        # Paginate the results
        paginated_posts = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Prepare the response
        posts_data = []
        for post in paginated_posts.items:
            post_dict = post.to_dict()
            post_dict['author'] = post.author.to_dict() if post.author else None
            if post.community_id:
                post_dict['community'] = post.community.to_dict()
            posts_data.append(post_dict)
        
        return jsonify({
            'posts': posts_data,
            'total': paginated_posts.total,
            'pages': paginated_posts.pages,
            'current_page': page,
            'has_next': paginated_posts.has_next,
            'has_prev': paginated_posts.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close() 