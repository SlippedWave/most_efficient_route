from flask import Blueprint
from app.blueprints.edit_user_info.update_info import UpdateInfoView
from app.blueprints.edit_user_info.change_password import ChangePasswordView 

edit_user_info = Blueprint(
    "edit_user_info", __name__, template_folder="templates/edit_user_info"
)

edit_user_info.add_url_rule(
    "/actualizar_informacion", view_func=UpdateInfoView.as_view("update_info")
)

edit_user_info.add_url_rule(
    "/cambiar_contrasena", view_func=ChangePasswordView.as_view("change_password")
)


class View:
    def get_blueprint(self):
        return edit_user_info
