from flask import Blueprint, render_template, redirect
from flask_login import login_user, current_user, logout_user

from app import bcrypt, db
from forms import RegisterForm, LoginForm
from models import User

auth = Blueprint('auth', __name__, url_prefix="/admin/auth")


@auth.get('/login')
@auth.post('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/admin/albums')
        else:
            return redirect('/')
    return render_template('admin/auth/login.html', form=form)


@auth.get('/register')
@auth.post('/register')
def register():
    if current_user.is_authenticated:
        return redirect('/admin')
    form = RegisterForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, firstName=form.firstName.data, lastName=form.lastName.data, password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        return redirect('/admin/albums')
    return render_template('admin/auth/register.html', form=form)


@auth.get('/logout')
def logout():
    logout_user()
    return redirect('/admin')

@auth.get('/account')
def logout():
    return render_template('admin/auth/account.html')
