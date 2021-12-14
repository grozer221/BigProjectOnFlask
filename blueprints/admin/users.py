import json

from flask import Blueprint, render_template, request, redirect
from flask_login import current_user

from app import db
from decorators import authAdmin
from models.models import User, Role

users = Blueprint('users', __name__, url_prefix="/admin/users")


@users.get('/')
@authAdmin
def index():
    users = db.session.query(User).filter(User.id != current_user.id)
    return render_template('admin/users/index.html', users=users, Role=Role)


@users.post('/updateRole')
@authAdmin
def updateRole():
    id = request.args.get('id')
    role = request.args.get('role')
    user = User.query.get(id)
    setattr(user, 'role', role)
    db.session.commit()
    return json.dumps(user)


@users.get('/delete/<int:id>')
@authAdmin
def delete(id: int):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/admin/users')
