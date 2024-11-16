from flask import Blueprint
from app.blueprints.manage_users.register_user import RegisterUserView
from app.blueprints.manage_users.manage_users import ManageUsersView
from app.blueprints.manage_users.edit_user import EditUserView

manage_users = Blueprint(
    "manage_users", __name__, template_folder="templates/manage_users"
)
manage_users.add_url_rule(
    "/administrar_usuarios", view_func=ManageUsersView.as_view("manage_users")
)
manage_users.add_url_rule(
    "/registrar_usuario", view_func=RegisterUserView.as_view("register_user")
)
manage_users.add_url_rule(
    "/editar_usuario/<int:id>", view_func=EditUserView.as_view("edit_user")
)


class View:
    def get_blueprint(self):
        return manage_users
