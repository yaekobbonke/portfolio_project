from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from website import db
import bcrypt


user_courses = db.Table(
    'user_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    """user model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password_hash = hashed_password.decode('utf-8')
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Course(db.Model):
    """model for storing  courses in a database
    """
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(50), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)
    users = db.relationship('User', secondary=user_courses, backref=db.backref('courses', lazy='dynamic'))

class Blog(db.Model):
    """model for storing animal health courses in a database
    """
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(30), nullable=False, default=datetime.utcnow())

class Program(db.Model):
    """Creates available programs"""
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    Code = db.Column(db.String(100))

class Book(db.Model):
    """model for storing bookks in a database.
    """
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    publication_date = db.Column(db.Date)
    
class Health(db.Model):
    """model for storing animal health courses in a database.
    """
    ___tablename__ = 'heath'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    
class Animal(db.Model):
    """model for storing animal science courses in a database.
    """
    __tablename__ = 'animal_science'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        """Convert the Animal object to a dictionary.
        """
        return {
            'id': self.id,
            'title': self.title
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Animal object from a dictionary.
        """
        return cls(
            id=data['id'],
            title=data['title']
        )

class Crop(db.Model):
    """model for storing natural science courses in a database.
    """
    __tablename__ = 'crop_science'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False) 
    
    def to_dict(self):
        """Convert the Crop object to a dictionary.
        """
        return {
            'id': self.id,
            'title': self.title
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Crop object from a dictionary.
        """
        return cls(
            id=data['id'],
            title=data['title']
        )
      

class Natural(db.Model):
    """model for storing animal science courses in a database.
    """
    __tablename__ = 'natural'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        """Convert the Natural object to a dictionary.
        """
        return {
            'id': self.id,
            'title': self.title
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Natural object from a dictionary.
        """
        return cls(
            id=data['id'],
            title=data['title']
        )
     
class Cooperative(db.Model):
    """model for storing animal health courses in a database.
    """
    ___tablename__ = 'cooperative'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    
    def to_dict(self):
        """Convert the Cooperative object to a dictionary.
        """
        return {
            'id': self.id,
            'title': self.title
        }
    @classmethod
    def from_dict(cls, data):
        """Create an Cooperative object from a dictionary.
        """
        return cls(
            id=data['id'],
            title=data['title']
        )

class News(db.Model):
    """Model for news articles."""
    __tablename__ = 'news_table'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
class Announcement(db.Model):
    """Model for announcements."""
    __tablename__ = 'announcement'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)