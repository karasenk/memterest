from flask import Blueprint, render_template, redirect
from forms.user import LoginForm
from data.db_session import create_session
from data.user import User


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
        return redirect('/')
    return render_template('login.html', form=form, title='Авторизация', current_user=None)
