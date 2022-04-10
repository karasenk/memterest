from flask_restful import Resource
from flask_login import current_user, login_required
from forms.pin import PinForm
from flask import render_template, make_response, redirect
from data.db_session import create_session
from data.board import Board
from data.pin import Pin
from data.category import Category


class PinListResource(Resource):
    @login_required
    def get(self):
        form = PinForm()
        db_sess = create_session()
        form.boards.choices = [b[0] for b in db_sess.query(
            Board.name).filter(Board.author_username == current_user.username).all()]
        return make_response(render_template('pin.html',
                                             form=form, title='Загрузка мема'))
    @login_required
    def post(self):
        form = PinForm()
        db_sess = create_session()
        board_id = db_sess.query(Board.id).filter(Board.name == form.boards.data)[0]
        ids = [i[0] for i in db_sess.query(Pin.id).all()]
        if not ids:
            pin_id = 1
        else:
            pin_id = max(ids) + 1
        category_id = db_sess.query(Category.id).filter(Category.name == form.category.data)[0]
        fname = f'mem{pin_id}.jpg'
        print(form.alt.data)
        pin = Pin(title=form.title.data,
                  mem_filename=fname,
                  alt=form.alt.data,
                  author_username=current_user.username,
                  categories=category_id,
                  source=form.source.data,
                  boards=board_id)
        db_sess.add(pin)
        db_sess.commit()
        f = open(fname, 'wb')
        f.write(form.mem.data.read())
        f.close()
        return make_response(redirect('/'))

