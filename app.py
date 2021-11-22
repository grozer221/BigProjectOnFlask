from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
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


db.create_all()

from blueprints.admin.albums import albums
from blueprints.admin.songs import songs
from blueprints.admin.auth import auth

app.register_blueprint(albums, url_prefix='/admin/albums')
app.register_blueprint(songs, url_prefix='/admin/songs')
app.register_blueprint(auth, url_prefix='/admin/auth')


@app.errorhandler(404)
def handle_404(e):
    return render_template('admin/error.html')


@app.errorhandler(500)
def handle_500(e):
    return render_template('admin/error.html')


if __name__ == '__main__':
    app.run(debug=True)
