import os

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '34qu3qpibc4uit3q4u9gqesdkngfmi9w4hq'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = '/admin/auth/login'
loginManager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)

# dont touch !!!!!!!!!!!!!!!!!!!!!!!!!!
from models.models import Album
from models.models import Song
from models.models import User
# dont touch !!!!!!!!!!!!!!!!!!!!!!!!!!

db.create_all()

from blueprints.admin.albums import albums
from blueprints.admin.songs import songs
from blueprints.admin.auth import auth
from blueprints.admin.users import users

app.register_blueprint(albums, url_prefix='/admin/albums')
app.register_blueprint(songs, url_prefix='/admin/songs')
app.register_blueprint(auth, url_prefix='/admin/auth')
app.register_blueprint(users, url_prefix='/admin/users')


@app.errorhandler(404)
def handle_404(e):
    return render_template('admin/error.html', errorCode=404)


@app.errorhandler(500)
def handle_500(e):
    return render_template('admin/error.html', errorCode=500)


if __name__ == '__main__':
    app.run(debug=True)
