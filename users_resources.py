from flask_restful import reqparse, abort, Resource
from forms.user import RegisterForm
from flask import render_template, make_response, redirect
from data.db_session import create_session
from data.user import User


class UsersListResource(Resource):
    def get(self):
        form = RegisterForm()
        return make_response(render_template('register.html',
                                             form=form, title='Регистрация'))

    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пользователь с такой почтой уже есть")
            if db_sess.query(User).filter(User.username == form.username.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Юзернейм уже занят")
            f = open(f'static/img/{form.username.data}_photo.jpg', 'wb')
            f.write(form.photo.data.read())
            f.close()
            user = User(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                username=form.username.data,
                photo_filename=f'static/img/{form.username.data}_photo',
                email=form.email.data,
                about=form.about.data

            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
