# Community package 
from flask import Blueprint
from .routes import init_app

community_bp = Blueprint('community_main', __name__)

def init_app(app):
    from .routes import init_app as init_routes
    init_routes(app) 