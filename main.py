from flask import Flask, render_template
from flask_restful import Api
import users_resources
import board_resources
from data.db_session import global_init
import user_api
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
api.add_resource(users_resources.UsersListResource, '/register')
api.add_resource(board_resources.BoardListResource, '/new_board')
app.register_blueprint(user_api.blueprint)


@app.route('/')
def base():
    return render_template('base.html', title='Мемтерест')


if __name__ == '__main__':
    global_init("db/memterest.db")
    app.run(port=8080, host='127.0.0.1')
