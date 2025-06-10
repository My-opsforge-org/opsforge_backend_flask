# Community routes package 
from flask import Blueprint

# Create a single blueprint for all community routes
community_bp = Blueprint('community', __name__)

# Import route modules after creating the blueprint
from . import create, get, join, leave

# Register routes
create.register_routes(community_bp)
get.register_routes(community_bp)
join.register_routes(community_bp)
leave.register_routes(community_bp) 