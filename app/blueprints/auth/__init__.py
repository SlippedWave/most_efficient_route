from flask import Blueprint
from app.blueprints.auth.login import LoginView
from app.blueprints.auth.logout import LogoutView

from app.blueprints.auth.recover_user import RecoverUserView
from app.blueprints.auth.reset_password import ResetPasswordView

auth = Blueprint("auth", __name__, template_folder="templates/auth")
auth.add_url_rule("/iniciar_sesion", view_func=LoginView.as_view("login"))
auth.add_url_rule("/cerrar_sesion", view_func=LogoutView.as_view("logout"))
auth.add_url_rule(
    "/iniciar_sesion/recuperar_usuario",
    view_func=RecoverUserView.as_view("recover_user"),
)
auth.add_url_rule(
    "/iniciar_sesion/cambiar_contrasena/<token>",
    view_func=ResetPasswordView.as_view("reset_password"),
)

from app import login_manager

login_manager.login_view = "auth.login"


class View:
    def get_blueprint(self):
        return auth
