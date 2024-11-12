from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Optional

class SetAdressInfoForm(FlaskForm):
    ADD_street = StringField('Calle', validators=[DataRequired()])
    ADD_ext_number = StringField('Número exterior', validators=[DataRequired()])
    ADD_int_number = StringField('Número interior', validators=[Optional()])
    ADD_neighborhood = StringField('Colonia', validators=[DataRequired()])
    ADD_zip_code = StringField('Código Postal', validators=[DataRequired()])
    ADD_city = StringField('Ciudad', validators=[DataRequired()])
    ADD_state = StringField('Estado', validators=[DataRequired()])