from wtforms.validators import DataRequired, InputRequired
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField


class AnecdoteForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    anecdote = TextAreaField('Анекдот', validators=[DataRequired()])
    source = StringField('Источник')
    boards = SelectField('Доски', validators=[DataRequired(), InputRequired()])
    category = SelectField('Категория', validators=[DataRequired()],
                           choices=['не определено', 'про котиков', 'про собачек',
                                    'про программистов', 'про художников',
                                    'про химиков', 'про Штирлица', 'про наркоманов'])
    submit = SubmitField('Сохранить')
