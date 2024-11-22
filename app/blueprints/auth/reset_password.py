import os
from itsdangerous import URLSafeTimedSerializer
from flask import render_template, flash, redirect, request, url_for
from flask.views import MethodView
from flask_login import current_user

from app.models import User
from app.extensions.database import db
from app.blueprints.auth.reset_password_form import ResetPasswordForm


def validate_reset_token(token, max_age=14400):
    serializer = URLSafeTimedSerializer(os.environ["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=os.environ["PASSWORD_RECOVERY_SALT"], max_age=max_age
        )
    except Exception:
        return None
    return email


class ResetPasswordView(MethodView):
    def get(self, token):

        if current_user.is_authenticated:
            flash(
                "No tienes que tener una sesión activa para acceder aquí.",
                "danger",
            )
            return redirect(request.args.get("next") or "/")

        email = validate_reset_token(token)

        if not email:
            flash(
                "El enlace para restablecer la contraseña no es válido o ha expirado.",
                "danger",
            )
            return redirect(url_for("auth.recover_user"))

        form = ResetPasswordForm()

        return render_template(
            "auth/reset_password.html",
            title="Reestablecer contraseña",
            form=form,
            url=url_for("auth.reset_password", token=token),
        )

    def post(self, token):

        if current_user.is_authenticated:
            flash(
                "No tienes que tener una sesión activa para acceder aquí.",
                "danger",
            )
            return redirect(request.args.get("next") or "/")

        email = validate_reset_token(token)

        if not email:
            flash(
                "El enlace para restablecer la contraseña no es válido o ha expirado.",
                "danger",
            )
            return redirect(url_for("auth.recover_user"))

        form = ResetPasswordForm()

        if form.validate_on_submit():

            user = User.query.filter_by(USR_email=email).first()
            if not user:
                flash("No se encontró un usuario con el correo asociado.", "danger")
                return redirect(url_for("auth.recover_user"))

            plain_password = form.plain_password.data
            user.set_password(plain_password)

            try:
                db.session.commit()
                flash(
                    "¡Tu contraseña ha sido actualizada exitosamente! Ahora puedes iniciar sesión.",
                    "success",
                )
                return redirect(url_for("auth.login"))
            except Exception as e:
                flash("Error al registrar los cambios", "error")

        flash("Hubo un error con el formulario.", "danger")
        return render_template(
            "auth/reset_password.html",
            title="Reestablecer contraseña",
            form=form,
            url=url_for("auth.reset_password")
        )
