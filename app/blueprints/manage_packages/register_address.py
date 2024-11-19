from flask import render_template, flash, url_for
from flask.views import MethodView

from app.models import Address
from app.blueprints.manage_packages.set_address_info_form import SetAdressInfoForm
from app.extensions.auth import require, has_permit_type
from app.extensions.database import db


class RegisterAddressView(MethodView):
    @require(has_permit_type("Administrador", "Almacenista"))
    def get(self):
        form = SetAdressInfoForm()

        return render_template(
            "manage_packages/set_address_info_form.html",
            form=form,
            url=url_for("manage_packages.register_address"),
        )

    def post(self):
        form = SetAdressInfoForm()

        if form.validate_on_submit():
            newAddress = Address(
                ADD_city= form.ADD_city.data,
                ADD_ext_number=form.ADD_ext_number.data,
                ADD_int_number=form.ADD_int_number.data,
                ADD_state=form.ADD_state.data,
                ADD_zip_code=form.ADD_zip_code.data,
                ADD_neighborhood=form.ADD_neighborhood.data,
                ADD_street=form.ADD_street.data
            )
            db.session.add(newAddress)
            db.session.commit()
            flash("Dirección registrada exitosamente!", "success")
            return 'success'
        
        flash("¡Se encontraron problemas en el registro!", "error")
        return render_template(
            "manage_packages/set_address_info_form.html",
            form=form,
            url=url_for("manage_packages.register_package"),
        )
