from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv
import secrets
from auth.models import db
from auth.routes import auth_bp
from explore import explore_bp, init_app

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # Initialize explore blueprint
    init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(explore_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
