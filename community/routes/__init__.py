# Community routes package 
from flask import Blueprint

community_bp = Blueprint('community', __name__)

from . import community_routes
from . import post_routes
from . import comment_routes
from . import reaction_routes
from . import bookmark_routes
from . import profile_posts_routes
from . import feed_routes

def init_app(app):
    app.register_blueprint(community_bp, url_prefix='/api')
    app.register_blueprint(community_routes.community_routes_bp, url_prefix='/api')
    app.register_blueprint(post_routes.post_bp, url_prefix='/api')
    app.register_blueprint(comment_routes.comment_bp, url_prefix='/api')
    app.register_blueprint(reaction_routes.reaction_bp, url_prefix='/api')
    app.register_blueprint(bookmark_routes.bookmark_bp, url_prefix='/api') 