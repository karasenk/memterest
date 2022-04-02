from flask import Flask
from flask_restful import Api

import users_resources
from data.db_session import global_init
import user_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
api.add_resource(users_resources.UsersListResource, '/register')
app.register_blueprint(user_api.blueprint)


if __name__ == '__main__':
    global_init("db/memterest.db")
    app.run(port=8080, host='127.0.0.1')
