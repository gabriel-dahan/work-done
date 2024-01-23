from . import __db as db

from flask_login import UserMixin
from sqlalchemy.orm import column_property

import time
from datetime import datetime

def current_time_millis():
    return round(time.time() * 1000)

class Unit(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, default = current_time_millis(), primary_key = True)
    content = db.Column(db.Text, nullable = False)
    done = db.Column(db.Boolean, nullable = False, default = False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

    # FOREIGN KEYS
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

class Thread(db.Model):
    __tablename__ = 'threads'

    id = db.Column(db.Integer, default = current_time_millis(), primary_key = True)
    title = db.Column(db.String(80), nullable = False)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

    # RELATIONSHIPS
    units = db.relationship('Unit', backref = 'thread', lazy = True) # One-to-many

    # FOREIGN KEYS
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __repr__(self) -> str:
        return f'Thread(id: {self.id}, title: {self.title})'

class Workspace(db.Model):
    __tablename__ = 'workspaces'

    id = db.Column(db.Integer, default = current_time_millis(), primary_key = True)
    title = db.Column(db.String(40), nullable = False)

    # RELATIONSHIPS
    threads = db.relationship('Thread', backref = 'workspace', lazy = True) # One-to-many

    # FOREIGN KEYS
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: float = db.Column(db.Integer, default = current_time_millis(), primary_key = True)
    name: str = db.Column(db.String(20), unique = True, nullable = False)
    passwd: str = db.Column(db.String(80), nullable = False)

    # RELATIONSHIPS
    workspaces = db.relationship('Workspace', backref = 'author', lazy = True) # One-to-many
    threads = db.relationship('Thread', backref = 'author', lazy = True) # One-to-many
    units = db.relationship('Unit', backref = 'author', lazy = True) # One-to-many

    def __repr__(self) -> str:
        return f'User(name: {self.name})'