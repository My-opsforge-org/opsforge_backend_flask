from flask import Blueprint

explore_bp = Blueprint('explore', __name__, url_prefix='/api/explore')

from .routes.geocode_routes import get_coordinates
from .routes.places_routes import get_places

def init_app(app):
    app.register_blueprint(explore_bp)