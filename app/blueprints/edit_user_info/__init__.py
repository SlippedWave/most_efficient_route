from flask import Blueprint
from app.blueprints.edit_user_info.update_info import UpdateInfoView

edit_user_info = Blueprint(
    "edit_user_info", __name__, template_folder="templates/edit_user_info"
)

edit_user_info.add_url_rule(
    "/actualizar_informacion", view_func=UpdateInfoView.as_view("edit_user_info")
)

class View:
    def get_blueprint(self):
        return edit_user_info
