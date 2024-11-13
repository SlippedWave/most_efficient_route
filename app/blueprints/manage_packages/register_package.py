from flask import render_template, flash, redirect, url_for
from flask.views import MethodView
from flask_login import current_user

from app.models import Package
from app.blueprints.manage_packages.set_package_info_form import SetPackageInfoForm
from app.extensions.auth import require, has_permit_type
from app.extensions.database import db


class RegisterPackageView(MethodView):
    @require(lambda: has_permit_type("Administrador"))
    def get(self):
        form = SetPackageInfoForm()

        return render_template(
            "manage_packages/set_package_info_form.html",
            form=form,
            url=url_for("manage_packages.register_package"),
        )

    def post(self):
        form = SetPackageInfoForm()

        if form.validate_on_submit():
            newPackage = Package(
                PCK_USR_modified_by=current_user.USR_userId,
                PCK_client_name=form.PCK_client_name.data,
                PCK_client_phone_num=form.PCK_client_phone_num.data,
                PCK_ST_statusId=form.status.data.ST_statusId,
                PCK_special_delivery_instructions=form.PCK_special_delivery_instructions.data,
                PCK_USR_assigned_to=form.PCK_USR_assigned_to.data,
                PCK_ADD_addressId=form.PCK_ADD_addressId.data,
            )
            db.session.add(newPackage)
            db.session.commit()
            flash("¡Usuario registrado exitosamente!", "success")
            return redirect(url_for("manage_users.manage_users"))

        flash("¡Se encontraron problemas en el registro!", "error")
        return render_template(
            "manage_packages/set_package_info_form.html",
            form=form,
            url=url_for("manage_packages.register_package"),
        )
