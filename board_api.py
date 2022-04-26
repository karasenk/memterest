from flask import Blueprint, render_template, abort
from data.db_session import create_session
from data.board import Board
from data.user import User
from data.pin import Pin
from data.anecdote import Anecdote


blueprint = Blueprint(
    'board_api',
    __name__,
    template_folder='templates')


@blueprint.route('/board/<int:board_id>')
def print_board(board_id):
    db_sess = create_session()
    board = db_sess.query(Board).filter(Board.id == board_id).all()
    if not board:
        abort(404)
    board = board[0]
    collaborators0 = db_sess.query(User).all()
    collaborators = []
    for c in collaborators0:
        if c.username in board.collaborators.split():
            collaborators.append(c)
    pins0 = db_sess.query(Pin)
    pins = []
    for pin in pins0:
        for b in pin.boards:
            if b.id == board.id:
                pins.append({'type': 'mem',
                             'mem': f'static/img/mem{pin.id}.jpg',
                             'alt': pin.alt,
                             'id': pin.id,
                             'title': pin.title,
                             'author': db_sess.query(User).filter(User.id == pin.user_id)[0]
                             })
                break
    anecs0 = db_sess.query(Anecdote)
    anecs = []
    for anec in anecs0:
        for b in anec.boards:
            if b.id == board.id:
                anecs.append({'type': 'anec',
                              'text': anec.text,
                              'id': anec.id,
                              'title': anec.title,
                              'author': db_sess.query(User).filter(User.id == anec.user_id)[0]
                              })
                break
    posts = anecs + pins
    return render_template('print_board.html', posts=posts,
                           title=board.name, collaborators=collaborators, board=board)
