from flask import render_template, flash, redirect, request, session, url_for
from flask.views import MethodView
from flask_login import login_user, current_user
from app.models import User
from app.blueprints.auth.login_form import LoginForm


class LoginView(MethodView):
    def get(self):
        # Check if the user is already authenticated
        if current_user.is_authenticated:
            return redirect(request.args.get('next') or url_for('index'))  # Use url_for for more flexibility
        form = LoginForm()
        return render_template('auth/login.html',
                               title='Sign In',
                               form=form)

    def post(self):
        # If the user is already authenticated, redirect
        if current_user.is_authenticated:
            return redirect(request.args.get('next') or url_for('index'))  # Use url_for for more flexibility

        form = LoginForm()
        if form.validate_on_submit():
            # Retrieve the user by username
            user = User.query.filter_by(USR_email=form.email.data).first()
            if user and user.check_password(form.password.data):
                if login_user(user, remember=form.remember_me.data):
                    # Enable session expiration only if user hasn't chosen to be remembered
                    session.permanent = not form.remember_me.data
                    flash('¡Inicio de sesión exitoso!', 'success')
                    session['remember_me'] = form.remember_me.data
                    return redirect(request.args.get('next') or '/')  # Use url_for for more flexibility
                else:
                    flash('¡Este usuario está deshabilitado!', 'error')
            else:
                flash('¡Contraseña incorrecta!', 'error')

        # Return the form with error messages
        return render_template('auth/login.html',
                               title='Sign In',
                               form=form)
