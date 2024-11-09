from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired()])
    password = PasswordField('contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme', default=False)
