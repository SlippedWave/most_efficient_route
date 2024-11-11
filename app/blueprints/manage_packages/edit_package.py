from flask import render_template, jsonify, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import current_user
from app.models import User, Status, Permit
from app.blueprints.manage_packages.edit_package_form import EditPackageForm
from app.extensions.database import db


class EditPackageView(MethodView):

    def get(self, id):
        user = User.query.get_or_404(id)
        form = EditPackageForm(obj=user)

        status_choices = [
            (status.ST_statusId, status.ST_value) for status in Status.query.all()
        ]
        permit_choices = [
            (permit.PMT_permitId, permit.PMT_type) for permit in Permit.query.all()
        ]

        form.status.choices = status_choices
        form.permit.choices = permit_choices

        if current_user.USR_userId == id:
            form.status.render_kw = {"class": "form-control", "disabled": "disabled"}

        return render_template("manage_users/set_user_info_form.html",
                                form=form,
                                url= url_for('manage_users.edit_user', id=user.USR_userId))

    def post(self, id):
        user = User.query.get_or_404(id)
        
        form = EditPackageForm(request.form, obj=user)

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
                return jsonify({"status": "error", "message": "Error al actualizar el usuario"})
        else:
            return jsonify({"status": "error", "message": "Formulario no válido", "errors": form.errors})