from flask import Blueprint, render_template, redirect, abort, request
from forms.user import LoginForm, NewPasswordForm
from data.db_session import create_session
from data.user import User
from flask_login import login_user, login_required, logout_user
import random
from message import send_message


blueprint = Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/login', methods=['GET'])
def login_get():
    form = LoginForm()
    return render_template('login.html', form=form, title='Авторизация', current_user=None)


@blueprint.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.email == form.email_or_username.data).first()
        if not user:
            user = session.query(User).filter(User.username == form.email_or_username.data).first()
        if not user:
            return render_template('login.html', form=form, title='Авторизация',
                                   message='Пользователь не найден', current_user=None)
        if not User.check_password(user, form.password.data):
            return render_template('login.html', form=form, title='Авторизация',
                                   message='Неверный пароль', current_user=None)
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('login.html', form=form, title='Авторизация', current_user=None)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@blueprint.route('/user/<int:user_id>')
def get_user_page(user_id):
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == user_id).all()
    if user:
        return render_template('print_user.html', title=user[0].username, user=user[0])
    abort(404)


@blueprint.route('/password_recovery', methods=['GET', 'POST'])
def password_recovery():
    if request.method == 'GET':
        return render_template('password_recovery.html', title='Восстановление пароля')
    session = create_session()
    user = session.query(User).filter(User.email == request.form['email']).all()
    if not user:
        return render_template('password_recovery.html', message=True, title='Восстановление пароля')
    user = user[0]
    code = random.randrange(1, 1000000000)
    while session.query(User).filter(User.code == code).all():
        code = random.randrange(1, 1000000000)
    user.code = code
    session.commit()
    send_message(user.email, f'Чтобы сбросить пароль - /password_reset/{code}', 'Сброс пароля')
    return redirect('/')


@blueprint.route('/password_reset/<int:code>', methods=['GET', 'POST'])
def password_reset(code):
    session = create_session()
    user = session.query(User).filter(User.code == code).all()
    if not user:
        abort(404)
    form = NewPasswordForm()
    if request.method == 'GET':
        return render_template('password_reset.html', form=form, title='Сброс пароля')
    if form.password.data != form.password_again.data:
        return render_template('password_reset.html', form=form,
                               title='Сброс пароля', message='Пароли не совпадают.')
    user[0].set_password(form.password.data)
    session.commit()
    return redirect('/login')
