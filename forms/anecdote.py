from wtforms.validators import DataRequired, InputRequired
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField


class AnecdoteForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    anecdote = FileField('Анекдот', validators=[DataRequired()])
    source = StringField('Источник')
    boards = SelectField('Доски', validators=[DataRequired(), InputRequired()])
    category = SelectField('Категория', validators=[DataRequired()],
                           choices=['про котиков', 'про собачек', 'про программистов',
                                    'про художников', 'про химиков', 'не определено'])
    submit = SubmitField('Сохранить')
