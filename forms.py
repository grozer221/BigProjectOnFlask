from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=50), Email()])
    firstName = StringField("Ім'я", validators=[DataRequired(), Length(min=2, max=50)])
    lastName = StringField('Прізвище', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Зареєструватися')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=50), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Увійти')


class AccountUpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=50), Email()])
    firstName = StringField("Ім'я", validators=[DataRequired(), Length(min=2, max=50)])
    lastName = StringField('Прізвище', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Оновити')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=50), Email()])
    submit = SubmitField('Змінити')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Змінити')

