import os
from flask import render_template, flash, url_for
from flask.views import MethodView
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask_login import current_user

from app.models import User
from app.blueprints.auth.recover_user_form import RecoverUserForm
from app.extensions.mail import mail


def generate_password_reset_token(email):
    serializer = URLSafeTimedSerializer(os.environ["SECRET_KEY"])
    return serializer.dumps(email, salt=os.environ["PASSWORD_RECOVERY_SALT"])


def generate_password_reset_link(email):
    token = generate_password_reset_token(email)
    return url_for("auth.reset_password", token=token, _external=True)


class RecoverUserView(MethodView):

    def get(self):

        if current_user.is_authenticated:
            flash(
                "No tienes que tener una sesión activa para acceder aquí.",
                "danger",
            )
            return redirect(request.args.get("next") or "/")

        form = RecoverUserForm()

        return render_template(
            "auth/recover_user.html", form=form, url=url_for("auth.recover_user")
        )

    def post(self):

        if current_user.is_authenticated:
            flash(
                "No tienes que tener una sesión activa para acceder aquí.",
                "danger",
            )
            return redirect(request.args.get("next") or "/")

        form = RecoverUserForm()
        if form.validate_on_submit():
            USR_email = form.email.data.strip()
            user = User.query.filter_by(USR_email=USR_email).first()
            if user:

                msg = Message(
                    subject="Reestablece tu contraseña de Beaver Deliver.",
                    sender=os.environ["MAIL_USERNAME"],
                    recipients=[USR_email],
                )
                msg.html = render_template(
                    "mail/restore_password_email.html",
                    name=user.USR_name,
                    url=generate_password_reset_link(USR_email),
                )
                mail.send(msg)

                flash("¡Ingresa el código que has recibido en tu correo!", "alert")
            else:
                flash(
                    "¡No se encontró una cuenta asociada al correo otorgado!", "danger"
                )

        flash("Hubo un error con el formulario.", "danger")
        return render_template(
            "auth/recover_user.html", form=form, url=url_for("auth.recover_user")
        )
