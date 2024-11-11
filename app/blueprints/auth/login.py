from flask import render_template, flash, redirect, request, session
from flask.views import MethodView
from flask_login import login_user, current_user
from app.models import User
from app.blueprints.auth.login_form import LoginForm


class LoginView(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(request.args.get('next') or '/')
        
        form = LoginForm()
        return render_template('auth/login.html',
                               title='Sign In',
                               form=form)

    def post(self):
        if current_user.is_authenticated:
            return redirect(request.args.get('next') or '/')
        
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(USR_email=form.email.data).first()
            if user and user.check_password(form.password.data):
                if user.is_active():       
                    login_user(user, remember=form.remember_me.data)
                    session.permanent = not form.remember_me.data
                    flash('¡Inicio de sesión exitoso!', 'success')
                    return redirect(request.args.get('next') or '/')
                else:
                    flash(user.status)
                    flash('¡Este usuario está deshabilitado', 'error')
            else:
                flash('¡Contraseña o correo incorrecto!', 'error')

        return render_template('auth/login.html',
                               title='Sign In',
                               form=form)
