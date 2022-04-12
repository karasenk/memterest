from flask import Blueprint, render_template, redirect
from data.db_session import create_session
from data.pin import Pin
from flask_login import login_user


blueprint = Blueprint(
    'pin_api',
    __name__,
    template_folder='templates')


@blueprint.route('/pins')
def print_pins():
    db_sess = create_session()
    pins = db_sess.query(Pin).order_by(Pin.id.desc()).limit(9)
    pins1 = []
    for pin in pins:
        pins1.append({'mem': f'static/img/mem{pin.id}.jpg',
                      'alt': pin.alt,
                      'id': pin.id})
    return render_template('pins.html', title='Все мемы', pins=pins)

