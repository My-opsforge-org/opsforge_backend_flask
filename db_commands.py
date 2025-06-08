from flask_migrate import Migrate, upgrade, init, migrate as flask_migrate
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)

def init_db():
    with app.app_context():
        init()

def create_migration(message):
    with app.app_context():
        flask_migrate(message=message)

def upgrade_db():
    with app.app_context():
        upgrade()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db_commands.py [init|migrate|upgrade]")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == 'init':
        init_db()
    elif command == 'migrate':
        message = sys.argv[2] if len(sys.argv) > 2 else "migration"
        create_migration(message)
    elif command == 'upgrade':
        upgrade_db()
    else:
        print("Unknown command. Use: init, migrate, or upgrade") 