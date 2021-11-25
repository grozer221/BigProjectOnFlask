from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from models import User


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=50), Email()])
    firstName = StringField("Ім'я", validators=[DataRequired(), Length(min=2, max=50)])
    lastName = StringField('Прізвище', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Зареєструватися')

    def validateEmail(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Користувач з введеним email уже існує')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=50), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=2, max=50)])
    remember = BooleanField("Запам'ятати")
    submit = SubmitField('Увійти')
