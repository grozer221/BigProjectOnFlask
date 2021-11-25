from flask_login import UserMixin

from app import db, loginManager

@loginManager.user_loader
def loadUser(userId):
    return User.query.get(int(userId))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120))
    lastName = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))


class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
