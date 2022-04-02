from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms import EmailField, BooleanField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = EmailField('Юзернейм', validators=[DataRequired()])
    firstname = StringField('Имя', validators=[DataRequired()])
    lastname = StringField('Фамилия')
    photo = FileField('Фото профиля')
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email_or_username = EmailField('Почта или юзернейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
