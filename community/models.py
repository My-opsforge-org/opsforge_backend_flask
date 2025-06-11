from datetime import datetime
from app import db

community_members = db.Table('community_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('community_id', db.Integer, db.ForeignKey('community.id'), primary_key=True)
)

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    members = db.relationship('User', secondary=community_members, backref=db.backref('communities_joined', lazy='dynamic'))
    posts = db.relationship('Post', backref='community', lazy='dynamic')

    def to_dict(self, include_members=False):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'members_count': len(self.members),
            'posts_count': self.posts.count()
        }
        if include_members:
            data['members'] = [user.id for user in self.members]
        return data

    def is_member(self, user_id):
        # Convert user_id to integer if it's a string
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        # Check if any member's ID matches the user_id
        return any(member.id == user_id for member in self.members)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=True)  # Made optional
    post_type = db.Column(db.String(20), nullable=False, default='profile')  # 'profile' or 'community'
    
    author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))
    images = db.relationship('Image', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    reactions = db.relationship('Reaction', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    bookmarks = db.relationship('Bookmark', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_comments=False):
        data = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author_id': self.author_id,
            'community_id': self.community_id,
            'post_type': self.post_type,
            'images': [image.to_dict() for image in self.images],
            'likes_count': self.reactions.filter_by(reaction_type='like').count(),
            'dislikes_count': self.reactions.filter_by(reaction_type='dislike').count(),
            'comments_count': self.comments.count(),
            'is_bookmarked': False  # Will be set by the route if needed
        }
        if include_comments:
            data['comments'] = [comment.to_dict() for comment in self.comments]
        return data

    def get_user_reaction(self, user_id):
        reaction = self.reactions.filter_by(user_id=user_id).first()
        return reaction.reaction_type if reaction else None

    def is_bookmarked_by(self, user_id):
        return self.bookmarks.filter_by(user_id=user_id).first() is not None

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    author = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))

    def to_dict(self, include_author=False):
        data = {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author_id': self.author_id,
            'post_id': self.post_id
        }
        if include_author:
            data['author'] = self.author.to_dict() if self.author else None
        return data

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reaction_type = db.Column(db.String(10), nullable=False)  # 'like' or 'dislike'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('reactions', lazy='dynamic'))
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_reaction'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'reaction_type': self.reaction_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id,
            'post_id': self.post_id
        }

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('bookmarks', lazy='dynamic'))
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_bookmark'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id,
            'post_id': self.post_id
        } 