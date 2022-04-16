import datetime

from flask import Blueprint, render_template, redirect, request
from data.db_session import create_session
from data.pin import Pin
from data.anecdote import Anecdote
from data.user import User
from data.category import Category
from data.board import Board
from flask_login import current_user, mixins


blueprint = Blueprint(
    'pin_api',
    __name__,
    template_folder='templates')


@blueprint.route('/')
@blueprint.route('/categories/<int:cat_id>')
def print_mems_and_anecs(cat_id=0):
    curus = current_user
    if curus.__class__ == mixins.AnonymousUserMixin:
        curus = None
    db_sess = create_session()
    pins = db_sess.query(Pin).order_by(Pin.id.desc()).all()
    anecs = db_sess.query(Anecdote).order_by(Anecdote.id.desc()).all()
    if cat_id == 0:
        title = 'Главная страница'
    else:
        cat = db_sess.query(Category).filter(Category.id == cat_id)[0]
        title = cat.name
    pins1 = []
    anecs1 = []
    if cat_id != 0:
        for pin in pins:
            for c in pin.categories:
                if c == cat:
                    pins1.append({'mem': f'static/img/mem{pin.id}.jpg',
                                  'alt': pin.alt,
                                  'id': pin.id,
                                  'title': pin.title,
                                  'author': db_sess.query(User).filter(User.id == pin.user_id)[0]
                                  })
        for anec in anecs:
            for c in anec.categories:
                if c == cat:
                    anecs1.append({'text': anec.text,
                                   'id': anec.id,
                                   'title': anec.title,
                                   'author': db_sess.query(User).filter(User.id == anec.user_id)[0]
                                   })
    else:
        for pin in pins:
            pins1.append({'mem': f'static/img/mem{pin.id}.jpg',
                          'alt': pin.alt,
                          'id': pin.id,
                          'title': pin.title,
                          'author': db_sess.query(User).filter(User.id == pin.user_id)[0]
                          })
        for anec in anecs:
            anecs1.append({'text': anec.text,
                           'id': anec.id,
                           'title': anec.title,
                           'author': db_sess.query(User).filter(User.id == anec.user_id)[0]
                           })
    return render_template('pins.html', title=title, pins=pins1, anecs=anecs1, current_user=curus)


@blueprint.route('/pin/<int:mem_id>', methods=['GET', 'POST'])
def print_mem(mem_id):
    db_sess = create_session()
    mem = db_sess.query(Pin).filter(Pin.id == mem_id)[0]
    username = db_sess.query(User.username).filter(User.id == mem.user_id)[0][0]
    boards = []
    for board in db_sess.query(Board).all():
        if board.user_id == current_user.id or \
                current_user.username in board.collaborators.split():
            boards.append(board)
    if request.method == 'POST':
        board = db_sess.query(Board).filter(Board.id == int(request.form['board']))[0]
        mem.boards.append(board)
        db_sess.commit()
    return render_template('print_pin.html', mem=mem, username=username,
                           current_user=current_user, title=mem.title, boards=boards)


@blueprint.route('/delete_mem/<int:mem_id>')
def delete_mem(mem_id):
    db_sess = create_session()
    mem = db_sess.query(Pin).filter(Pin.id == mem_id)[0]
    db_sess.delete(mem)
    db_sess.commit()
    return redirect('/')
