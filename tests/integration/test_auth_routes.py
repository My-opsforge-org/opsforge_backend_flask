import pytest
import json
from auth.models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class TestAuthRoutes:
    """Integration tests for authentication routes."""
    
    def test_user_registration_success(self, client, db_session):
        """Test successful user registration."""
        user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        response = client.post('/api/register', json=user_data)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'User created successfully'
        
        # Verify user was created in database
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert user.name == 'Test User'
    
    def test_user_registration_duplicate_email(self, client, db_session):
        """Test user registration with duplicate email."""
        # Create first user
        user = User(
            name='Existing User',
            email='test@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8')
        )
        db_session.add(user)
        db_session.commit()
        
        # Try to register with same email
        response = client.post('/api/register', json={
            'name': 'New User',
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Email already exists' in data['error']
    
    def test_user_login_success(self, client, db_session):
        """Test successful user login."""
        # Create user first
        user = User(
            name='Test User',
            email='test@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8')
        )
        db_session.add(user)
        db_session.commit()
        
        # Login
        response = client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert data['message'] == 'Login successful'
    
    def test_user_login_invalid_credentials(self, client, db_session):
        """Test user login with invalid credentials."""
        # Create user first
        user = User(
            name='Test User',
            email='test@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8')
        )
        db_session.add(user)
        db_session.commit()
        
        # Wrong password
        response = client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Invalid email or password' in data['error']
        
        # Non-existent email
        response = client.post('/api/login', json={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 401
    
    def test_user_login_missing_fields(self, client):
        """Test user login with missing fields."""
        response = client.post('/api/login', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 400
        
        response = client.post('/api/login', json={
            'password': 'password123'
        })
        assert response.status_code == 400
    
    def test_user_logout_success(self, client, db_session):
        """Test successful user logout."""
        # Create and login user
        user = User(
            name='Test User',
            email='test@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8')
        )
        db_session.add(user)
        db_session.commit()
        
        login_response = client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token = login_response.get_json()['access_token']
        
        # Logout
        response = client.post('/api/logout', headers={
            'Authorization': f'Bearer {token}'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'Successfully logged out' in data['message']
    
    def test_user_logout_no_token(self, client):
        """Test user logout without token."""
        response = client.post('/api/logout')
        
        assert response.status_code == 401
    
    def test_get_profile_success(self, client, db_session):
        """Test successful profile retrieval."""
        # Create and login user
        user = User(
            name='Test User',
            email='test@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8'),
            bio='Test bio',
            age=25,
            gender='male',
            sun_sign='aries'
        )
        db_session.add(user)
        db_session.commit()
        
        login_response = client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token = login_response.get_json()['access_token']
        
        # Get profile
        response = client.get('/api/profile', headers={
            'Authorization': f'Bearer {token}'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Test User'
        assert data['email'] == 'test@example.com'
        assert data['bio'] == 'Test bio'
        assert data['age'] == 25
        assert data['gender'] == 'male'
        assert data['sun_sign'] == 'aries'
    
    def test_get_profile_no_token(self, client):
        """Test profile retrieval without token."""
        response = client.get('/api/profile')
        
        assert response.status_code == 401
    
    def test_update_profile_invalid_data(self, client, db_session):
        """Test profile update with invalid data."""
        # Create and login user
        user = User(
            name='Test User',
            email='test@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8')
        )
        db_session.add(user)
        db_session.commit()
        
        login_response = client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token = login_response.get_json()['access_token']
        
        # Invalid age
        response = client.put('/api/profile', 
                            json={'age': 150},
                            headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 400
        
        # Invalid gender
        response = client.put('/api/profile', 
                            json={'gender': 'invalid'},
                            headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 400
    
    def test_follow_user_success(self, client, db_session):
        """Test successful user follow."""
        # Create two users
        user1 = User(
            name='User 1',
            email='user1@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8')
        )
        user2 = User(
            name='User 2',
            email='user2@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8')
        )
        db_session.add_all([user1, user2])
        db_session.commit()
        
        # Login user1
        login_response = client.post('/api/login', json={
            'email': 'user1@example.com',
            'password': 'password123'
        })
        token = login_response.get_json()['access_token']
        
        # Follow user2
        response = client.post(f'/api/follow/{user2.id}', 
                             headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'followed successfully' in data['message']
    
    def test_follow_nonexistent_user(self, client, db_session):
        """Test following a non-existent user."""
        # Create user
        user = User(
            name='Test User',
            email='test@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8')
        )
        db_session.add(user)
        db_session.commit()
        
        # Login
        login_response = client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token = login_response.get_json()['access_token']
        
        # Try to follow non-existent user
        response = client.post('/api/follow/999', 
                             headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 404
    
    def test_unfollow_user_success(self, client, db_session):
        """Test successful user unfollow."""
        # Create two users
        user1 = User(
            name='User 1',
            email='user1@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8')
        )
        user2 = User(
            name='User 2',
            email='user2@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8')
        )
        db_session.add_all([user1, user2])
        db_session.commit()
        
        # Make user1 follow user2
        user1.follow(user2)
        db_session.commit()
        
        # Login user1
        login_response = client.post('/api/login', json={
            'email': 'user1@example.com',
            'password': 'password123'
        })
        token = login_response.get_json()['access_token']
        
        # Unfollow user2
        response = client.delete(f'/api/follow/{user2.id}', 
                               headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'unfollowed successfully' in data['message'] 