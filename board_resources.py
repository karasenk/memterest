from flask_restful import Resource
from flask_login import current_user, mixins
from forms.board import BoardForm
from flask import render_template, make_response, redirect
from data.db_session import create_session
from data.board import Board
from data.user import User


class BoardListResource(Resource):
    def get(self):
        if current_user.__class__ == mixins.AnonymousUserMixin:
            return redirect("/")
        form = BoardForm()
        return make_response(render_template('board.html', form=form,
                                             title='Создание доски'))

    def post(self):
        if current_user.__class__ == mixins.AnonymousUserMixin:
            return redirect("/")
        form = BoardForm()
        db_sess = create_session()
        usernames = form.collaborators.data.split()
        message = []
        all_usernames = [u[0] for u in db_sess.query(User.username)]
        print(all_usernames)
        for username in usernames:
            if username not in all_usernames:
                message.append(f'Пользователя с юзернеймом {username} не существует')
        if message:
            return make_response(render_template('board.html', form=form,
                                                 title='Создание доски', message='\n'.join(message)))
        board = Board(name=form.title.data,
                      description=form.description.data,
                      collaborators=form.collaborators.data,
                      user_id=current_user.id)
        db_sess.add(board)
        db_sess.commit()
        return make_response(redirect('/'))
