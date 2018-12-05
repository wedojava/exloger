from datetime import datetime
from time import time
from hashlib import md5
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class LogImported(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    sender_address = db.Column(db.String(255), index=True)
    recipient_address = db.Column(db.String(255))
    recipient_count = db.Column(db.Integer)
    return_path = db.Column(db.String(255))
    client_hostname = db.Column(db.String(255))
    client_ip = db.Column(db.String(100))
    server_hostname = db.Column(db.String(255))
    server_ip = db.Column(db.String(100))
    original_client_ip = db.Column(db.String(100))
    original_server_ip = db.Column(db.String(100))
    event_id = db.Column(db.String(50))
    total_bytes = db.Column(db.Integer)
    connector_id = db.Column(db.String(50))
    message_subject = db.Column(db.String(255))
    source = db.Column(db.String(50))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)