from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, InputRequired


class PinForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    photo = FileField('Мем', validators=[DataRequired()])
    alt = StringField('Описание')
    source = StringField('Источник')
    boards = SelectField('Доски', validators=[DataRequired(), InputRequired()])
    category = SelectField('Категория', validators=[DataRequired()],
                           choices=['про котиков', 'про собачек', 'про программистов',
                                    'про художников', 'про химиков', 'не определено'])
    submit = SubmitField('Сохранить')
