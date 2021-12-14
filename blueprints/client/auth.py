from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from app import bcrypt, db, mail
from forms import RegisterForm, LoginForm, AccountUpdateForm, RequestResetForm, ResetPasswordForm
from models.models import User, Role

clientAuth = Blueprint('clientAuth', __name__, url_prefix="/auth")


@clientAuth.get('/login')
@clientAuth.post('/login')
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect('/')
        else:
            return render_template('client/auth/login.html', form=form, commonError='Неправильний email або пароль', Role=Role)
    return render_template('client/auth/login.html', form=form, Role=Role)


@clientAuth.get('/register')
@clientAuth.post('/register')
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            return render_template('client/auth/register.html', form=form,
                                   commonError='Користувач з введеним email уже існує', Role=Role)

        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, firstName=form.firstName.data, lastName=form.lastName.data,
                    password=hashedPassword, Role=Role)
        db.session.add(user)
        db.session.commit()
        return redirect('/auth/login')
    return render_template('client/auth/register.html', form=form, Role=Role)


@clientAuth.get('/logout')
def logout():
    logout_user()
    return redirect('/')


@clientAuth.get('/account')
@clientAuth.post('/account')
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.firstName = form.firstName.data
        current_user.lastName = form.lastName.data
        db.session.commit()
        return render_template('client/auth/account.html', form=form, commonSuccess='Дані оновлено', Role=Role)
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
    return render_template('client/auth/account.html', form=form, Role=Role)


def sendResetEmail(user):
    token = user.getResetToken()
    message = Message('Відновлення паролю', sender='noreply@demo.com', recipients=[user.email])
    message.body = f'''Щоб відонвити пароль перейдіть по посиланню 
    {url_for('auth.resetToken', token=token, _external=True)}
    '''
    mail.send(message)


@clientAuth.get('/reset-password')
@clientAuth.post('/reset-password')
def resetPassword():
    if current_user.is_authenticated:
        return redirect('/')
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return render_template('client/auth/reset-password.html', form=form,
                                   commonError='Користувач з введеним email не існує', Role=Role)
        else:
            sendResetEmail(user)
            return render_template('client/auth/reset-password.html', form=form,
                                   info='Запит на зміну паролю надісланий на пошту', Role=Role)
    return render_template('/client/auth/reset-password.html', form=form, Role=Role)


@clientAuth.get('/reset-password/<token>')
@clientAuth.post('/reset-password/<token>')
def resetToken(token):
    if current_user.is_authenticated:
        return redirect('/')
    user = User.verifyResetToken(token)
    if user is None:
        return redirect('/auth/reset-password')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashedPassword
        db.session.commit()
        return redirect('/auth/login')
    return render_template('client/auth/reset-token.html', form=form, Role=Role)
