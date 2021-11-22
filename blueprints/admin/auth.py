from flask import Blueprint, render_template

from models.models import User

auth = Blueprint('auth', __name__, url_prefix="/admin/auth")


@auth.route('/')
def index():
    return render_template('admin/auth/index.html', users=User.query.all())
