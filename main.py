from flask import Flask, render_template
from flask_login import LoginManager, current_user, mixins
from flask_restful import Api
import pin_resources
import users_resources
import board_resources
from data.db_session import global_init, create_session
from data.user import User
import user_api
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
api.add_resource(users_resources.UsersListResource, '/register')
api.add_resource(board_resources.BoardListResource, '/new_board')
api.add_resource(pin_resources.PinListResource, '/new_pin')
app.register_blueprint(user_api.blueprint)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def base():
    curus = current_user
    if curus.__class__ == mixins.AnonymousUserMixin:
        curus = None
    return render_template('base.html', title='Мемтерест', current_user=curus)


if __name__ == '__main__':
    global_init("db/memterest.db")
    app.run(port=8080, host='127.0.0.1')
