from flask import Blueprint
from app.blueprints.home.home import HomeView

home = Blueprint('home', __name__, template_folder='templates/home')
home.add_url_rule('/', view_func=HomeView.as_view('home'))

class View:
    def get_blueprint(self):
        return home