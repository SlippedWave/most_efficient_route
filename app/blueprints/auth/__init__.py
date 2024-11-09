from flask import Blueprint
from app.blueprints.auth.login import LoginView
from app.blueprints.auth.logout import LogoutView

auth = Blueprint('auth', __name__, template_folder='templates/auth')
auth.add_url_rule('/iniciar_sesion', view_func=LoginView.as_view('login'))
auth.add_url_rule('/cerrar_sesion', view_func=LogoutView.as_view('logout'))

from app import login_manager
login_manager.login_view = 'auth.login'

class View:
    def get_blueprint(self):
        return auth