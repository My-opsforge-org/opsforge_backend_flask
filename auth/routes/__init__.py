from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import login_routes
from . import register_routes
from . import logout_routes
from . import protected_routes
from . import profile_routes 