from flask import render_template, jsonify, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import current_user
from wtforms.validators import Optional, Regexp
from datetime import datetime

from app.models import User
from app.blueprints.manage_users.set_user_info_form import SetUserInfoForm
from app.extensions.database import db
from app.extensions.auth import require, has_permit_type

class EditUserView(MethodView):
    @require(has_permit_type("Administrador"))
    def get(self, id):
        user = User.query.get_or_404(id)
        form = SetUserInfoForm(obj=user)

        form.plain_password.validators = [
            Optional(),
            Regexp('^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{8,})')
        ]
        form.USR_email.render_kw = {"class": "form-control", "readonly": "readonly"}
        if current_user.USR_userId == id:
            form.status.render_kw = {"class": "form-control", "disabled": "disabled"}

        return render_template(
            "manage_users/set_user_info_form.html",
            form=form,
            url=url_for("manage_users.edit_user", id=user.USR_userId),
        )

    def post(self, id):
        user = User.query.get_or_404(id)

        form = SetUserInfoForm(request.form, obj=user)
        
        form.plain_password.validators = [
            Optional(),
            Regexp('^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{8,})')
        ]

        if form.validate_on_submit():
            user.USR_email = form.USR_email.data
            user.USR_name = form.USR_name.data
            user.USR_last_name = form.USR_last_name.data
            user.USR_telephone = form.USR_telephone.data
            user.USR_address = form.USR_address.data       
            user.USR_PER_permitId = form.permit.data.PMT_permitId
            user.USR_ST_statusId = form.status.data.ST_statusId
            user.USR_gender = form.USR_gender.data
            user.USR_modified_by = current_user.USR_userId
            user.USR_last_modified = datetime.now()


            plain_password = form.plain_password.data

            if plain_password:
                user.set_password(plain_password)

            try:
                db.session.commit()
                flash("¡Cambios realizados exitosamente!", "success")
                return redirect(url_for("manage_users.manage_users"))
            except Exception as e:
                flash("Error al registrar los cambios", "error")

        else:
            flash("Formulario inválido", "error")

