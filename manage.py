from flask.cli import FlaskGroup
from app import create_app, db
from flask_migrate import Migrate

app = create_app()
cli = FlaskGroup(create_app=lambda info: app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    cli() 
    