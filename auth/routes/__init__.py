from flask import Blueprint

# Create the blueprint
auth_bp = Blueprint('auth', __name__)

# Import routes after creating blueprint to avoid circular imports
from . import login_routes
from . import register_routes
from . import logout_routes
from . import protected_routes
from . import profile_routes
from . import follow_routes

def init_app(app):
    # Register the blueprint with the app
    app.register_blueprint(auth_bp, url_prefix='/api') 