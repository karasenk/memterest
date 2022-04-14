from flask import Blueprint, render_template, redirect
from data.db_session import create_session
from data.anecdote import Anecdote
from data.board import Board
from data.user import User
from data.category import Category
from forms.anecdote import AnecdoteForm
from flask_login import current_user, mixins


blueprint = Blueprint(
    'anecdote_api',
    __name__,
    template_folder='templates')


@blueprint.route('/new_anecdote', methods=['GET'])
def get_anecdote():
    if current_user.__class__ == mixins.AnonymousUserMixin:
        return redirect("/")
    form = AnecdoteForm()
    db_sess = create_session()
    form.boards.choices = [b[0] for b in db_sess.query(
        Board.name).filter(Board.user_id == current_user.id).all()]
    return render_template('anecdote.html', form=form, title='Загрузка анекдота')


@blueprint.route('/new_anecdote', methods=['POST'])
def post_anecdote():
    form = AnecdoteForm()
    db_sess = create_session()
    board = db_sess.query(Board).filter(Board.name == form.boards.data)[0]
    category = db_sess.query(Category).filter(Category.name == form.category.data)[0]
    anec = Anecdote()
    anec.title = form.title.data
    anec.text = form.anecdote.data
    anec.source = form.source.data
    anec.user_id = current_user.id
    anec.categories.append(category)
    anec.boards.append(board)
    db_sess.add(anec)
    db_sess.commit()
    return redirect('/')


@blueprint.route('/anec/<int:anec_id>')
def print_anecdote(anec_id):
    db_sess = create_session()
    anec = db_sess.query(Anecdote).filter(Anecdote.id == anec_id)[0]
    username = db_sess.query(User.username).filter(User.id == anec.user_id)[0][0]
    return render_template('print_anecdote.html', anec=anec, username=username,
                           current_user=current_user, title=anec.title)


@blueprint.route('/delete_anec/<int:anec_id>')
def delete_anec(anec_id):
    db_sess = create_session()
    anec = db_sess.query(Anecdote).filter(Anecdote.id == anec_id)[0]
    db_sess.delete(anec)
    db_sess.commit()
    return redirect('/')
