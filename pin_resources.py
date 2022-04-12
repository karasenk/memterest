from flask_restful import Resource
from flask_login import current_user, mixins
from forms.pin import PinForm
from flask import render_template, make_response, redirect
from data.db_session import create_session
from data.board import Board
from data.pin import Pin
from data.category import Category


class PinListResource(Resource):
    def get(self):
        if current_user.__class__ == mixins.AnonymousUserMixin:
            return redirect("/")
        form = PinForm()
        db_sess = create_session()
        form.boards.choices = [b[0] for b in db_sess.query(
            Board.name).filter(Board.user_id == current_user.id).all()]
        return make_response(render_template('pin.html',
                                             form=form, title='Загрузка мема'))

    def post(self):
        if current_user.__class__ == mixins.AnonymousUserMixin:
            return redirect("/")
        form = PinForm()
        db_sess = create_session()
        board = db_sess.query(Board).filter(Board.name == form.boards.data)[0]
        ids = [i[0] for i in db_sess.query(Pin.id).all()]
        if not ids:
            pin_id = 1
        else:
            pin_id = max(ids) + 1
        category = db_sess.query(Category).filter(Category.name == form.category.data)[0]
        fname = f'static/img/mem{pin_id}.jpg'

        pin = Pin()
        pin.title = form.title.data
        pin.mem_filename = fname
        pin.alt = form.alt.data
        pin.author_username = current_user.username
        pin.categories.append(category)
        pin.source = form.source.data
        pin.boards.append(board)

        db_sess.add(pin)
        db_sess.commit()
        f = open(fname, 'wb')
        f.write(form.mem.data.read())
        f.close()
        return make_response(redirect('/'))

