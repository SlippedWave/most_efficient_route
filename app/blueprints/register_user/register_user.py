from flask import render_template, flash, redirect, request, session
from flask.views import MethodView
from flask_login import current_user

from app.models import User
from app.blueprints.register_user.register_user_form import RegisterUserForm
from app.extensions.auth import require, has_permit_type

class RegisterUserView(MethodView):
    @require(lambda: has_permit_type("Administrador"))
    def get(self):
        form = RegisterUserForm()
        return render_template(
            "register_user/register_user.html", title="Registrar nuevo usuario", form=form, form_token=session['form_token']
        )

    def post(self):
        form = RegisterUserForm()
        existing_user = User.query.filter_by(USR_email=form.email.data).first()
        if existing_user:
            flash("¡El correo electrónico ya está registrado!", "error")
        else:
            newUser = User(
                USR_email=form.email.data,
                plain_password=form.plain_password.data,
                USR_name=form.name.data,
                USR_last_name=form.last_name.data,
                USR_telephone=form.telephone.data,
                USR_address=form.address.data,
                USR_PER_permitId=form.permit.data,
                USR_ST_statusId=form.status.data,
            )
            newUser.save()
            flash("¡Usuario registrado exitosamente!", "success")

            form.email.data = ''
            form.plain_password.data = ''
            form.name.data = ''
            form.last_name.data = ''
            form.telephone.data = ''
            form.address.data = ''
            form.permit.data = ''
            form.status.data = ''

            return render_template(
                "register_user/register_user.html", title="Registrar nuevo usuario", form=form
            )
        
        return render_template(
            "register_user/register_user.html", title="Registrar nuevo usuario", form=form
        )
