from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import json

# Creates SQLAlchemy object in memory (no files yet)
db = SQLAlchemy()

# Post is a class (template) for creating blog post objects
# Inherits from Model which lives inside db object (db.Model)
# and gives access to db.Column and other SQLAlchemy methods
class Post(db.Model):
    # Explicitly sets table name to 'posts' (plural), without this SQLAlchemy defaults to 'post'
    # Each model class creates a separate table in the database
    __tablename__ = 'posts'

    id         = db.Column(db.Integer, primary_key=True) # unique id, auto-incremented by SQLite
    title      = db.Column(db.String(200), nullable=False)
    content    = db.Column(db.Text, nullable=False) # text = unlimited length (up to 1 billion chars in SQLite)
    category   = db.Column(db.String(100), nullable=False)
    _tags      = db.Column('tags', db.Text, default='[]') # private field, converted to list/text automatically via getter/setter below
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) # set on creation
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), # set on creation
                           onupdate=lambda: datetime.now(timezone.utc)) # updated on every change

    # @property must be defined first — declares 'tags' object that @tags.setter references
    @property # reading a post - property is called
    def tags(self):
        return json.loads(self._tags) # converts JSON string from db to Python list

    # references 'tags' object that was declared above
    @tags.setter # creating/updating a post - setter is called
    def tags(self, value):
        self._tags = json.dumps(value) # converts Python list to JSON string for db storage

    # converts Post object to dict so Flask can serialize it to JSON
    # avoids repeating the same dict structure in every endpoint in app.py
    # Z = UTC timezone indicator (ISO 8601 standard)
    def to_dict(self):
        return {
            'id':        self.id,
            'title':     self.title,
            'content':   self.content,
            'category':  self.category,
            'tags':      self.tags,
            'createdAt': self.created_at.isoformat() + 'Z',
            'updatedAt': self.updated_at.isoformat() + 'Z',
        }