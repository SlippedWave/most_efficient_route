from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms.validators import DataRequired, Email

class RecoverUserForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])