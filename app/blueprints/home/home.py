from flask import render_template
from flask.views import MethodView
from flask_login import current_user

class HomeView(MethodView):
    def get(self):
        return render_template('home/index.html', authenticated=current_user.is_authenticated)
