from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Regexp, EqualTo, Optional


class EditUserInfoForm(FlaskForm):
    USR_telephone = StringField(
        "Teléfono", validators=[DataRequired(), Regexp("^\d{10}$")]
    )
    USR_address = StringField("Dirección", validators=[DataRequired()])
    plain_password = PasswordField(
        "Nueva Contraseña",
        validators=[
            Optional(),
            Regexp(
                '^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{8,})',
                message="La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula y un carácter especial.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar Contraseña",
        validators=[
            EqualTo("plain_password", message="Las contraseñas deben ser iguales.")
        ],
    )
