from flask_login import UserMixin
from apps import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profiles = db.relationship('Profile', backref='userprofile', uselist=False)

    def __str__(self):
        return f"{self.username}"
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    address = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return f"{self.age}"
    
    def __init__(self, age, address, user):
        self.age = age
        self.address = address
        self.user = user
