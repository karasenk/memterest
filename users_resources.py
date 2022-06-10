from flask_restful import Resource
from forms.user import RegisterForm
from flask import render_template, make_response, redirect, request
from data.db_session import create_session
from data.user import User
from data.email_check import EmailCode
from message import send_message
from PIL import Image
import io
import random


def email_check(form):
    if not form.email.data:
        return make_response(render_template('register.html', form=form,
                                             title='Регистрация', message='Для начала введите почту'))
    sess = create_session()
    if sess.query(User).filter(User.email == form.email.data).first():
        return make_response(render_template('register.html', form=form, title='Регистрация',
                                             message='Пользователь с такой почтой уже зарегистрирован'))
    code = random.randrange(1, 1000000000)
    em = sess.query(EmailCode).filter(EmailCode.email == form.email.data).first()
    if em:
        em.code = code
    else:
        sess.add(EmailCode(email=form.email.data, code=code))
    sess.commit()
    try:
        send_message(form.email.data, f'Введите в специальное поле одноразовый код: {code}', 'Код для регистрации')
    except Exception as ex:
        print(ex)
    return make_response(render_template('register.html', form=form, title='Регистрация'))


class UsersListResource(Resource):
    def get(self):
        form = RegisterForm()
        return make_response(render_template('register.html', form=form, title='Регистрация', current_user=None))

    def post(self):
        form = RegisterForm()
        if 'send_code' in request.form.keys():
            return email_check(form)
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return make_response(render_template('register.html',
                                                     form=form, title='Регистрация', current_user=None,
                                                     message="Пароли не совпадают"))
            db_sess = create_session()
            em = db_sess.query(EmailCode).filter(EmailCode.email == form.email.data and
                                                 EmailCode.code == form.email.code).all()
            if em:
                db_sess.delete(em[0])
                db_sess.commit()
            else:
                return make_response(render_template('register.html', form=form,
                                                     message='Введён неверный код подтверждения'))
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
                about=form.about.data,
                code=0
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
        text = '''Добро пожаловать в Мемтерест!\nВы успешно зарегистрировались на нашем сайте и теперь можете:
        - создавать доски и сохранять на них мемы и анекдоты
        - загружать на сайт мемы и анекдоты
        - искать мемы и анекдоты по категориям'''
        send_message(form.email.data, text, 'приветствие', 'static/img/greeting.png')
        return make_response(redirect('/login'))
