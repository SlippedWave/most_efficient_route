from flask import render_template, jsonify, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import current_user

from app.models import User, Status, Package
from app.blueprints.manage_packages.set_package_info_form import SetPackageInfoForm
from app.extensions.database import db


class EditPackageView(MethodView):

    def get(self, id):
        package = Package.query.get_or_404(id)
        form = SetPackageInfoForm(obj=package)

        return render_template(
            "manage_packages/set_package_info_form.html",
            form=form,
            url=url_for("manage_packages.edit_package", id=package.PCK_packageId),
        )

    def post(self, id):
        user = User.query.get_or_404(id)

        form = SetPackageInfoForm(request.form, obj=user)

        if form.validate_on_submit():
            user.USR_email = form.USR_email.data
            user.USR_name = form.USR_name.data
            user.USR_last_name = form.USR_last_name.data
            user.USR_telephone = form.USR_telephone.data
            user.USR_address = form.USR_address.data

            user.USR_PER_permitId = form.permit.data.PMT_permitId
            user.USR_ST_statusId = form.status.data.ST_statusId

            plain_password = form.plain_password.data

            if plain_password:
                user.set_password(plain_password)

            try:
                db.session.commit()
                flash("¡Usuario registrado exitosamente!", "success")
                return redirect(url_for("manage_users.manage_users"))
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
