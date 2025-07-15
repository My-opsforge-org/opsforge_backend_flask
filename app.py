from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

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
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_size": 20,
        "max_overflow": 30,
        "pool_timeout": 30,
    }

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Ensure sessions are always removed after each request
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    # Register JWT callbacks
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        from auth.models import TokenBlocklist
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    # Import blueprints
    from auth.routes import auth_bp, init_app as init_auth
    from explore import explore_bp, init_app as init_explore
    from community import community_bp, init_app as init_community

    # Initialize blueprints
    init_auth(app)
    init_explore(app)
    init_community(app)

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000)) ## for deployment
    app.run(host='0.0.0.0', port=port) ## for deployment
    # app.run(host='0.0.0.0', port=5000, debug=True) ## for local development
