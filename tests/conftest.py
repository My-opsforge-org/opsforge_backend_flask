import pytest
import os
import tempfile
from app import create_app, db
from auth.models import User, TokenBlocklist
from community.models import Post, Comment, Reaction, Bookmark, Community, Image
from faker import Faker

fake = Faker()

class Config:
    """Test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key'
    JWT_SECRET_KEY = 'test-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = False  # Disable token expiration for testing

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.from_object(Config)
    
    # Create a temporary file to store the database
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def db_session(app):
    """Database session for testing."""
    with app.app_context():
        yield db.session

# Helper functions for creating test data
def create_test_user(db_session, **kwargs):
    """Create a test user with default or custom values."""
    from werkzeug.security import generate_password_hash
    
    user_data = {
        'name': kwargs.get('name', fake.name()),
        'email': kwargs.get('email', fake.email()),
        'password': kwargs.get('password', generate_password_hash('password123')),
        'avatarUrl': kwargs.get('avatarUrl', fake.image_url()),
        'bio': kwargs.get('bio', fake.text(max_nb_chars=200)),
        'age': kwargs.get('age', fake.random_int(min=18, max=80)),
        'gender': kwargs.get('gender', fake.random_element(elements=('male', 'female', 'other'))),
        'sun_sign': kwargs.get('sun_sign', fake.random_element(elements=[
            'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
            'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
        ])),
        'interests': kwargs.get('interests', '["travel", "photography"]'),
        'latitude': kwargs.get('latitude', fake.latitude()),
        'longitude': kwargs.get('longitude', fake.longitude())
    }
    
    user = User(**user_data)
    db_session.add(user)
    db_session.commit()
    return user

def create_test_post(db_session, author_id, **kwargs):
    """Create a test post with default or custom values."""
    post_data = {
        'title': kwargs.get('title', fake.sentence()),
        'content': kwargs.get('content', fake.text(max_nb_chars=500)),
        'author_id': author_id,
        'community_id': kwargs.get('community_id'),
        'post_type': kwargs.get('post_type', 'profile')
    }
    
    post = Post(**post_data)
    db_session.add(post)
    db_session.commit()
    return post

def create_test_community(db_session, **kwargs):
    """Create a test community with default or custom values."""
    community_data = {
        'name': kwargs.get('name', fake.company()),
        'description': kwargs.get('description', fake.text(max_nb_chars=300))
    }
    
    community = Community(**community_data)
    db_session.add(community)
    db_session.commit()
    return community

def create_test_image(db_session, post_id, **kwargs):
    """Create a test image with default or custom values."""
    image_data = {
        'url': kwargs.get('url', fake.image_url()),
        'post_id': post_id
    }
    
    image = Image(**image_data)
    db_session.add(image)
    db_session.commit()
    return image

# Fixtures for test data
@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    return create_test_user(db_session)

@pytest.fixture
def sample_users(db_session):
    """Create multiple sample users for testing."""
    return [create_test_user(db_session) for _ in range(5)]

@pytest.fixture
def sample_post(db_session, sample_user):
    """Create a sample post for testing."""
    return create_test_post(db_session, sample_user.id)

@pytest.fixture
def sample_community(db_session):
    """Create a sample community for testing."""
    return create_test_community(db_session)

@pytest.fixture
def auth_headers(client, sample_user):
    """Get authentication headers for a user."""
    # Register and login the user
    response = client.post('/api/register', json={
        'name': sample_user.name,
        'email': sample_user.email,
        'password': 'testpassword123'
    })
    
    response = client.post('/api/login', json={
        'email': sample_user.email,
        'password': 'testpassword123'
    })
    
    token = response.json.get('access_token')
    return {'Authorization': f'Bearer {token}'}

 