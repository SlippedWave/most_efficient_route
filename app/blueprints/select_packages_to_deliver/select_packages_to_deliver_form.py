from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired


class SelectPackagesToDeliverForm(FlaskForm):
    PCK_packagesId = HiddenField(
        "Selecciona los paquetes que vas a entregar", validators=[DataRequired()]
    )
