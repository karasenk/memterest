import datetime

from flask import Blueprint, render_template, redirect
from data.db_session import create_session
from data.pin import Pin
from data.user import User
from flask_login import current_user, mixins


blueprint = Blueprint(
    'pin_api',
    __name__,
    template_folder='templates')


@blueprint.route('/')
def print_pins():
    curus = current_user
    if curus.__class__ == mixins.AnonymousUserMixin:
        curus = None
    db_sess = create_session()
    pins = db_sess.query(Pin).order_by(Pin.id.desc()).limit(9)
    pins1 = []
    for pin in pins:
        pins1.append({'mem': f'static/img/mem{pin.id}.jpg',
                      'alt': pin.alt,
                      'id': pin.id,
                      'title': pin.title,
                      'author': db_sess.query(User).filter(User.id == pin.user_id)[0]
                      })
    return render_template('pins.html', title='Все мемы', pins=pins1, current_user=curus)
