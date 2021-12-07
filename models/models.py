from datetime import datetime
from enum import Enum

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db, loginManager, app


class Role(Enum):
    admin = 'admin'
    user = 'user'


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120))
    lastName = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.Enum(Role), default=Role.user)

    def getResetToken(self, expiresSec=1800):
        s = Serializer(app.config['SECRET_KEY'], expiresSec)
        return s.dumps({'userId': self.id}).decode('utf-8')

    @staticmethod
    def verifyResetToken(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            userId = s.loads(token)['userId']
        except:
            return None
        return User.query.get(userId)


class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    src = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    songs = relationship('Song', backref='song', cascade="all,delete")


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    album_id = db.Column(db.Integer, ForeignKey('albums.id'))
