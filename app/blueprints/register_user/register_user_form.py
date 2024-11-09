from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp

class RegisterUserForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    telephone = StringField('Teléfono', validators=[DataRequired(), Regexp('^\d{10}$')])
    plain_password = PasswordField('Contraseña', validators=[DataRequired(), Regexp()])
    name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    address = StringField('Dirección', validators=[DataRequired()])
    status = IntegerField('Estado', validators=[DataRequired()])
    permit = IntegerField('Tipo de usuario', validators=[DataRequired()])
    