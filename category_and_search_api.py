from flask import Blueprint, render_template, request, redirect
from data.db_session import create_session
from data.category import Category
from data.pin import Pin
from data.anecdote import Anecdote
from data.user import User
from flask_login import current_user, mixins

blueprint = Blueprint(
    'category_api',
    __name__,
    template_folder='templates')


@blueprint.route('/categories', methods=['GET', 'POST'])
def select_category():
    curus = current_user
    if curus.__class__ == mixins.AnonymousUserMixin:
        curus = None
    db_sess = create_session()
    if request.method == 'GET':
        categories = db_sess.query(Category).all()
        return render_template('select_category.html', categories=categories, title='Категории', current_user=curus)
    return redirect(f'/categories/{int(request.form["category"])}')


@blueprint.route('/search', methods=['GET', 'POST'])
def search():
    curus = current_user
    if curus.__class__ == mixins.AnonymousUserMixin:
        curus = None

    if request.method == 'GET':
        return render_template('search.html', title='Поиск', current_user=curus)
    db_sess = create_session()
    mems = []
    anecs = []
    to_find = request.form['to_find'].lower()
    for pin in db_sess.query(Pin).all():
        if to_find in pin.title.lower() or to_find in pin.alt.lower():
            mems.append({'mem': f'static/img/mem{pin.id}.jpg',
                         'alt': pin.alt,
                         'id': pin.id,
                         'title': pin.title,
                         'author': db_sess.query(User).filter(User.id == pin.user_id)[0]
                         })
    for anec in db_sess.query(Anecdote).all():
        if to_find in anec.title.lower() or to_find in anec.text.lower():
            anecs.append({'text': anec.text,
                          'id': anec.id,
                          'title': anec.title,
                          'author': db_sess.query(User).filter(User.id == anec.user_id)[0]
                          })
    return render_template('pins.html', title='Результаты поиска', anecs=anecs, pins=mems, current_user=curus)
