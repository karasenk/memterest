from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PinForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    alt = StringField('Описание')
    boards = StringField('Доски', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
