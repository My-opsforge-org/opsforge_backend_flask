# This file makes the explore directory a Python package 

from flask import Blueprint

explore_bp = Blueprint('explore', __name__, url_prefix='/api')

# Import routes
from .routes.geocode_routes import get_coordinates
from .routes.places_routes import get_places

def init_app(app):
    app.register_blueprint(explore_bp, url_prefix='/api/explore')
    app.register_blueprint(explore_bp, url_prefix='/api/places') 