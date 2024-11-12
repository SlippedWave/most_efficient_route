from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired, Regexp
from wtforms_sqlalchemy.orm import QuerySelectField
from app.models import Status

class SetPackageInfoForm(FlaskForm):
    PCK_client_name = StringField('Nombre del cliente', validators=[DataRequired()])
    PCK_client_phone_num = StringField('Teléfono', validators=[DataRequired(), Regexp('^\d{10}$')])
    status = QuerySelectField(
        'Estado', 
        query_factory=lambda: Status.query.filter_by(ST_status_type=0).all(), 
        get_label='ST_value', 
        validators=[DataRequired()]
    )
    assigned_to_user = HiddenField('Selecciona al usuario', validators=[DataRequired()])
    address = HiddenField('Ingresa la dirección', validators=[DataRequired()])
