from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired, Regexp, Optional
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
    PCK_USR_assigned_to = HiddenField('Selecciona al usuario', validators=[DataRequired()])
    PCK_ADD_addressId = HiddenField('Ingresa la dirección', validators=[DataRequired()])
    PCK_special_delivery_instructions = StringField('Indicaciones especiales', validators=[Optional()])
