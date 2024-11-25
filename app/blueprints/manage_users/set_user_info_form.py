from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Regexp, Optional

from wtforms_sqlalchemy.orm import QuerySelectField
from app.models import Status, Permit


class SetUserInfoForm(FlaskForm):
    USR_email = StringField("Correo electrónico", validators=[DataRequired(), Email()])
    USR_telephone = StringField(
        "Teléfono", validators=[DataRequired(), Regexp("^\d{10}$")]
    )
    plain_password = PasswordField(
        "Contraseña",
        validators=[
            Optional(),
            Regexp('^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{8,})'),
        ],
    )
    USR_name = StringField("Nombre", validators=[DataRequired()])
    USR_last_name = StringField("Apellido", validators=[DataRequired()])
    USR_address = StringField("Dirección", validators=[DataRequired()])
    USR_gender = SelectField(
        "Género",
        choices=[("0", "Masculino"), ("1", "Femenino"), ("2", "Otro")],
        validators=[DataRequired()],
    )
    status = QuerySelectField(
        "Estado",
        query_factory=lambda: Status.query.filter_by(ST_status_type=1).all(),
        get_label="ST_value",
        validators=[DataRequired()],
    )
    permit = QuerySelectField(
        "Tipo de usuario",
        query_factory=lambda: Permit.query.all(),
        get_label="PMT_type",
        validators=[DataRequired()],
    )
