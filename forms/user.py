from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms import EmailField, BooleanField, FileField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField('Юзернейм', validators=[DataRequired()])
    firstname = StringField('Имя', validators=[DataRequired()])
    lastname = StringField('Фамилия')
    photo = FileField('Фото профиля')
    email = EmailField('Почта', validators=[DataRequired()])
    code = IntegerField('Код подтверждения')
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email_or_username = StringField('Почта или юзернейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class NewPasswordForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
