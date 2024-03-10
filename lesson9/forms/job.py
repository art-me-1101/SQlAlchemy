from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    work_size = IntegerField("Время работы (в часах)", validators=[DataRequired()])
    collaborators = StringField("Участники", validators=[DataRequired()])
    submit = SubmitField('Применить')