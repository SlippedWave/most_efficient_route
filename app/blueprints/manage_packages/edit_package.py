from flask import render_template, jsonify, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import current_user

from app.models import Package
from app.blueprints.manage_packages.set_package_info_form import SetPackageInfoForm
from app.extensions.database import db
from app.extensions.auth import require, has_permit_type


class EditPackageView(MethodView):
    @require(has_permit_type("Administrador", "Almacenista"))
    def get(self, id):
        package = Package.query.get_or_404(id)
        form = SetPackageInfoForm(obj=package)

        return render_template(
            "manage_packages/set_package_info_form.html",
            form=form,
            url=url_for("manage_packages.edit_package", id=package.PCK_packageId),
        )

    def post(self, id):
        package = Package.query.get_or_404(id)

        form = SetPackageInfoForm(request.form, obj=package)

        if form.validate_on_submit():

            package.PCK_USR_modified_by = current_user.USR_userId
            package.PCK_client_name = form.PCK_client_name.data
            package.PCK_client_phone_num = form.PCK_client_phone_num.data
            package.PCK_ST_statusId = form.status.data.ST_statusId
            package.PCK_special_delivery_instructions = (
                form.PCK_special_delivery_instructions.data
            )

            assigned_to_user = form.PCK_USR_assigned_to.data
            address = form.PCK_ADD_addressId.data

            if assigned_to_user:
                package.PCK_USR_assigned_to = assigned_to_user

            if address:
                package.PCK_ADD_addressId = address

            try:
                db.session.commit()
                flash("¡Usuario registrado exitosamente!", "success")
                return redirect(url_for("manage_packages.manage_packages"))
            except Exception as e:
                print(f"Error updating user: {e}")
                return jsonify(
                    {"status": "error", "message": "Error al actualizar el usuario"}
                )
        else:
            return jsonify(
                {
                    "status": "error",
                    "message": "Formulario no válido",
                    "errors": form.errors,
                }
            )
