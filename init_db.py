from app import create_app
from auth.models import db

app = create_app()
with app.app_context():
    db.drop_all()  # This will drop all existing tables
    db.create_all()  # This will create new tables with the updated schema
    print("Database initialized successfully!") 