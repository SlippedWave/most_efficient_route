from flask import Blueprint, render_template
from app.blueprints.home.home import HomeView

home = Blueprint('home', __name__, template_folder='templates/home')

@home.route('/')
def splash():
    return render_template('splash.html')

# Ruta para la página principal
home.add_url_rule('/home', view_func=HomeView.as_view('home'))

class View:
    def get_blueprint(self):
        return home
