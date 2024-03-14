from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired


class DepartForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    members = StringField("Участники", validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()] )
    submit = SubmitField('Применить')