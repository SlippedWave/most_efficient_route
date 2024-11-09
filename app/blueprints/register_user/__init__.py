from flask import Blueprint
from app.blueprints.register_user.register_user import RegisterUserView

register_user = Blueprint('register_user', __name__, template_folder='templates/register_user')
register_user.add_url_rule('/registrar_usuario', view_func=RegisterUserView.as_view('register_user'))