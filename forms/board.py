from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BoardForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание')
    collaborators = StringField('Юзернеймы соавторов')
    submit = SubmitField('Сохранить')
