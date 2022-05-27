from flask import Blueprint, render_template, redirect, request, abort
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
@blueprint.route('/categories/<int:cat_id>/<int:page_num>')
@blueprint.route('/<int:page_num>')
def print_mems_and_anecs(cat_id=0, page_num=0):
    curus = current_user
    if curus.__class__ == mixins.AnonymousUserMixin:
        curus = None
    db_sess = create_session()
    pins = db_sess.query(Pin).all()[::-1]
    anecs = db_sess.query(Anecdote).all()[::-1]
    if cat_id == 0:
        title = 'Главная страница'
    else:
        cat = db_sess.query(Category).filter(Category.id == cat_id)[0]
        title = cat.name
    pins1 = []
    anecs1 = []
    if cat_id != 0:
        p = []
        for pin in pins:
            for c in pin.categories:
                if c == cat:
                    p.append(pin)
                    break
        a = []
        for anec in anecs:
            for c in anec.categories:
                if c == cat:
                    a.append(anec)
        pins = p
        anecs = a
    if 4 * page_num < len(pins):
        for pin in pins[4 * page_num:]:
            pins1.append({'type': 'mem',
                          'mem': f'static/img/mem{pin.id}.jpg',
                          'alt': pin.alt,
                          'id': pin.id,
                          'title': pin.title,
                          'author': db_sess.query(User).filter(User.id == pin.user_id)[0]
                          })
            if len(pins1) == 4:
                break
    if 4 * page_num < len(anecs):
        for anec in anecs[4 * page_num:]:
            anecs1.append({'type': 'anec',
                           'text': anec.text,
                           'id': anec.id,
                           'title': anec.title,
                           'author': db_sess.query(User).filter(User.id == anec.user_id)[0]
                           })
            if len(anecs1) == 4:
                break
    posts = pins1 + anecs1
    posts = list(sorted(posts, key=lambda x: x['id']))[::-1]
    back = page_num - 1
    if (page_num + 1) * 4 >= len(anecs) and (page_num + 1) * 4 >= len(pins):
        forward = -1
    else:
        forward = page_num + 1
    return render_template('pins.html', title=title, posts=posts, current_user=curus, back=back, forward=forward, cat=cat_id)


@blueprint.route('/pin/<int:mem_id>', methods=['GET', 'POST'])
def print_mem(mem_id):
    curus = current_user
    if curus.__class__ == mixins.AnonymousUserMixin:
        curus = None

    db_sess = create_session()
    mem = db_sess.query(Pin).filter(Pin.id == mem_id).all()
    if mem:
        mem = mem[0]
        username = db_sess.query(User.username).filter(User.id == mem.user_id)[0][0]
        boards = []
        if curus:
            for board in db_sess.query(Board).all():
                if board.user_id == curus.id or \
                        curus.username in board.collaborators.split():
                    boards.append(board)
        if request.method == 'POST':
            board = db_sess.query(Board).filter(Board.id == int(request.form['board']))[0]
            mem.boards.append(board)
            db_sess.commit()
        return render_template('print_pin.html', mem=mem, username=username,
                               current_user=curus, title=mem.title, boards=boards)
    abort(404)


@blueprint.route('/delete_mem/<int:mem_id>')
def delete_mem(mem_id):
    db_sess = create_session()
    mem = db_sess.query(Pin).filter(Pin.id == mem_id)[0]
    db_sess.delete(mem)
    db_sess.commit()
    return redirect('/')
