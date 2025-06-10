from datetime import datetime
import json
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    avatarUrl = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    sun_sign = db.Column(db.String(20), nullable=True)
    interests = db.Column(db.Text, nullable=True)  # Store as JSON string
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'
    
    def to_dict(self):
        try:
            interests = json.loads(self.interests) if self.interests else []
        except json.JSONDecodeError:
            interests = []
            
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'avatarUrl': self.avatarUrl,
            'bio': self.bio,
            'age': self.age,
            'gender': self.gender,
            'sun_sign': self.sun_sign,
            'interests': interests,
            'location': {
                'lat': self.latitude,
                'lng': self.longitude
            } if self.latitude is not None and self.longitude is not None else None,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None
        }

    def update_from_dict(self, data):
        """Update user fields from a dictionary, with validation."""
        if 'name' in data:
            self.name = data['name']
        if 'avatarUrl' in data:
            self.avatarUrl = data['avatarUrl']
        if 'bio' in data:
            self.bio = data['bio']
        if 'age' in data:
            try:
                age = int(data['age'])
                if age < 0 or age > 120:
                    raise ValueError("Age must be between 0 and 120")
                self.age = age
            except (ValueError, TypeError):
                raise ValueError("Invalid age value")
        if 'gender' in data:
            gender = str(data['gender']).lower()
            if gender not in ['male', 'female', 'other']:
                raise ValueError("Invalid gender value")
            self.gender = gender
        if 'sun_sign' in data:
            sun_sign = str(data['sun_sign']).lower()
            valid_signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                          'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
            if sun_sign not in valid_signs:
                raise ValueError("Invalid sun sign")
            self.sun_sign = sun_sign
        if 'interests' in data:
            try:
                self.interests = json.dumps(data['interests'])
            except (TypeError, ValueError):
                raise ValueError("Invalid interests format")
        if 'location' in data:
            location = data['location']
            if isinstance(location, dict):
                try:
                    lat = float(location.get('lat', 0))
                    lng = float(location.get('lng', 0))
                    if -90 <= lat <= 90 and -180 <= lng <= 180:
                        self.latitude = lat
                        self.longitude = lng
                    else:
                        raise ValueError("Invalid latitude/longitude values")
                except (ValueError, TypeError):
                    raise ValueError("Invalid location format")

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 