import pytest
import json
from auth.models import User, TokenBlocklist
from werkzeug.security import generate_password_hash, check_password_hash

class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation(self, db_session):
        """Test user creation with valid data."""
        user = User(
            name="Test User",
            email="test@example.com",
            password=generate_password_hash("password123"),
            bio="Test bio",
            age=25,
            gender="male",
            sun_sign="aries"
        )
        
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert check_password_hash(user.password, "password123")
        assert user.bio == "Test bio"
        assert user.age == 25
        assert user.gender == "male"
        assert user.sun_sign == "aries"
    
    def test_user_to_dict(self, db_session):
        """Test user to_dict method."""
        user = User(
            name="Test User",
            email="test@example.com",
            password=generate_password_hash("password123"),
            bio="Test bio",
            age=25,
            gender="male",
            sun_sign="aries",
            interests=json.dumps(["travel", "photography"]),
            latitude=40.7128,
            longitude=-74.0060
        )
        
        db_session.add(user)
        db_session.commit()
        
        user_dict = user.to_dict()
        
        assert user_dict['name'] == "Test User"
        assert user_dict['email'] == "test@example.com"
        assert user_dict['bio'] == "Test bio"
        assert user_dict['age'] == 25
        assert user_dict['gender'] == "male"
        assert user_dict['sun_sign'] == "aries"
        assert user_dict['interests'] == ["travel", "photography"]
        assert user_dict['location']['lat'] == 40.7128
        assert user_dict['location']['lng'] == -74.0060
        assert 'password' not in user_dict
        assert 'followers_count' in user_dict
        assert 'following_count' in user_dict
    
    def test_update_from_dict_invalid_age(self, db_session):
        """Test update_from_dict method with invalid age."""
        user = User(
            name="Test User",
            email="test@example.com",
            password=generate_password_hash("password123")
        )
        
        db_session.add(user)
        db_session.commit()
        
        with pytest.raises(ValueError, match="Age must be between 0 and 120"):
            user.update_from_dict({'age': 150})
        
        with pytest.raises(ValueError, match="Invalid age value"):
            user.update_from_dict({'age': 'invalid'})
    
    def test_update_from_dict_invalid_gender(self, db_session):
        """Test update_from_dict method with invalid gender."""
        user = User(
            name="Test User",
            email="test@example.com",
            password=generate_password_hash("password123")
        )
        
        db_session.add(user)
        db_session.commit()
        
        with pytest.raises(ValueError, match="Invalid gender value"):
            user.update_from_dict({'gender': 'invalid'})
    
    def test_update_from_dict_invalid_sun_sign(self, db_session):
        """Test update_from_dict method with invalid sun sign."""
        user = User(
            name="Test User",
            email="test@example.com",
            password=generate_password_hash("password123")
        )
        
        db_session.add(user)
        db_session.commit()
        
        with pytest.raises(ValueError, match="Invalid sun sign"):
            user.update_from_dict({'sun_sign': 'invalid'})
    
    def test_follow_unfollow_functionality(self, db_session):
        """Test follow and unfollow functionality."""
        user1 = User(
            name="User 1",
            email="user1@example.com",
            password=generate_password_hash("password123")
        )
        user2 = User(
            name="User 2",
            email="user2@example.com",
            password=generate_password_hash("password123")
        )
        
        db_session.add_all([user1, user2])
        db_session.commit()
        
        # Test follow
        assert user1.follow(user2) is True
        assert user1.is_following(user2) is True
        assert user2.followers.count() == 1
        assert user1.following.count() == 1
        
        # Test follow again (should return False)
        assert user1.follow(user2) is False
        
        # Test unfollow
        assert user1.unfollow(user2) is True
        assert user1.is_following(user2) is False
        assert user2.followers.count() == 0
        assert user1.following.count() == 0
        
        # Test unfollow again (should return False)
        assert user1.unfollow(user2) is False
    
    def test_self_follow_prevention(self, db_session):
        """Test that users cannot follow themselves."""
        user = User(
            name="Test User",
            email="test@example.com",
            password=generate_password_hash("password123")
        )
        
        db_session.add(user)
        db_session.commit()
        
        # Users should not be able to follow themselves
        assert user.follow(user) is False
        assert user.is_following(user) is False

class TestTokenBlocklistModel:
    """Test cases for TokenBlocklist model."""
    
    def test_token_blocklist_creation(self, db_session):
        """Test token blocklist creation."""
        token = TokenBlocklist(jti="test-jti-123")
        
        db_session.add(token)
        db_session.commit()
        
        assert token.id is not None
        assert token.jti == "test-jti-123"
        assert token.created_at is not None
    
    def test_token_blocklist_unique_jti(self, db_session):
        """Test that JTI must be unique."""
        token1 = TokenBlocklist(jti="test-jti-123")
        token2 = TokenBlocklist(jti="test-jti-123")
        
        db_session.add(token1)
        db_session.commit()
        
        with pytest.raises(Exception):  # SQLAlchemy will raise an integrity error
            db_session.add(token2)
            db_session.commit() 