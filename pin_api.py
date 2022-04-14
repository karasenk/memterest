import datetime

from flask import Blueprint, render_template, redirect
from data.db_session import create_session
from data.pin import Pin
from data.anecdote import Anecdote
from data.user import User
from flask_login import current_user, mixins


blueprint = Blueprint(
    'pin_api',
    __name__,
    template_folder='templates')


@blueprint.route('/')
def print_mems_and_anecs():
    curus = current_user
    if curus.__class__ == mixins.AnonymousUserMixin:
        curus = None
    db_sess = create_session()
    pins = db_sess.query(Pin).order_by(Pin.id.desc())
    anecs = db_sess.query(Anecdote).order_by(Anecdote.id.desc())
    pins1 = []
    for pin in pins:
        pins1.append({'mem': f'static/img/mem{pin.id}.jpg',
                      'alt': pin.alt,
                      'id': pin.id,
                      'title': pin.title,
                      'author': db_sess.query(User).filter(User.id == pin.user_id)[0]
                      })
    anecs1 = []
    for anec in anecs:
        anecs1.append({'text': anec.text,
                       'id': anec.id,
                       'title': anec.title,
                       'author': db_sess.query(User).filter(User.id == anec.user_id)[0]
                       })
    return render_template('pins.html', title='Главная страница', pins=pins1, anecs=anecs1, current_user=curus)


@blueprint.route('/pin/<int:mem_id>')
def print_mem(mem_id):
    db_sess = create_session()
    mem = db_sess.query(Pin).filter(Pin.id == mem_id)[0]
    username = db_sess.query(User.username).filter(User.id == mem.user_id)[0][0]
    return render_template('print_pin.html', mem=mem, username=username,
                           current_user=current_user, title=mem.title)


@blueprint.route('/delete_mem/<int:mem_id>')
def delete_mem(mem_id):
    db_sess = create_session()
    mem = db_sess.query(Pin).filter(Pin.id == mem_id)[0]
    db_sess.delete(mem)
    db_sess.commit()
    return redirect('/')
