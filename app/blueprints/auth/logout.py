from flask import flash, redirect, url_for
from flask.views import MethodView
from flask_login import logout_user, login_required

class LogoutView(MethodView):
    @login_required
    def get(self):
        logout_user()
        flash('¡Hasta pronto!', 'success')  
        return redirect(url_for('index')) 
