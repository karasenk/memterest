from flask_restful import reqparse, abort, Resource
from forms.user import RegisterForm
from flask import render_template, make_response, redirect
from data.db_session import create_session
from data.user import User
from message import send_message
from PIL import Image
import io


class UsersListResource(Resource):
    def get(self):
        form = RegisterForm()
        return make_response(render_template('register.html',
                                             form=form, title='Регистрация', current_user=None))

    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return make_response(render_template('register.html',
                                                     form=form, title='Регистрация', current_user=None,
                                                     message="Пароли не совпадают"))
            db_sess = create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return make_response(render_template('register.html',
                                                     form=form, title='Регистрация', current_user=None,
                                                     message="Пользователь с такой почтой уже есть"))
            if db_sess.query(User).filter(User.username == form.username.data).first():
                return make_response(render_template('register.html',
                                                     form=form, title='Регистрация', current_user=None,
                                                     message="Юзернейм уже занят"))
            if ' ' in form.username.data.strip():
                return make_response(render_template('register.html',
                                                     form=form, title='Регистрация', current_user=None,
                                                     message="В юзернейме не должны использоваться пробелы"))

            if form.photo.data:
                im = Image.open(io.BytesIO(form.photo.data.read()))
                sz = min(im.height, im.width)
                im.crop((0, 0, sz, sz)).save(f'static/img/{form.username.data}_photo.jpg', quality=100)
                fname = f'static/img/{form.username.data}_photo.jpg'
            else:
                fname = f'static/img/defaultavatar.png'
            user = User(
                firstname=form.firstname.data.strip(),
                lastname=form.lastname.data.strip(),
                username=form.username.data.strip(),
                photo_filename=fname,
                email=form.email.data.strip(),
                about=form.about.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
        text = '''Добро пожаловать в Мемтерест!\nВы успешно зарегистрировались на нашем сайте и теперь можете:
        - создавать доски и сохранять на них мемы и анекдоты
        - загружать на сайт мемы и анекдоты
        - искать мемы и анекдоты по категориям
        (Вы этого всего, конечно, пока не можете, но это пока)'''
        send_message(form.email.data, text, 'приветствие', 'static/img/greeting.png')
        return make_response(redirect('/login'))
