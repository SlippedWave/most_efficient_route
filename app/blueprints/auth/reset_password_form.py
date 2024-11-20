from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired, Regexp, EqualTo


class ResetPasswordForm(FlaskForm):
    plain_password = PasswordField(
        "Nueva Contraseña",
        validators=[
            DataRequired(),
            Regexp(
                '^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{8,})',
                message="La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula y un carácter especial.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar Contraseña",
        validators=[
            DataRequired(),
            EqualTo("plain_password", message="Las contraseñas deben ser iguales."),
        ],
    )
