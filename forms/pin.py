from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired


class PinForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    mem = FileField('Мем', validators=[DataRequired()])
    alt = StringField('Описание', validators=[DataRequired()])
    source = StringField('Источник')
    boards = SelectField('Доски', validators=[DataRequired()])
    category = SelectField('Категория', validators=[DataRequired()],
                           choices=['про котиков', 'про собачек', 'про программистов',
                                    'про художников', 'про химиков', 'не определено'])
    submit = SubmitField('Сохранить')
