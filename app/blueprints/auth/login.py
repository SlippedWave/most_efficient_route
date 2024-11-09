import uuid

from flask import render_template, flash, redirect, request, session, url_for
from flask.views import MethodView
from flask_login import login_user, current_user

from app.models import User
from app.blueprints.auth.login_form import LoginForm


class LoginView(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(request.args.get('next') or '/') 
        form = LoginForm()
        session['form_token'] = str(uuid.uuid4())  
        return render_template('auth/login.html',
                               title='Sign In',
                               form=form)

    def post(self):
 
        if current_user.is_authenticated:
            return redirect(request.args.get('next') or '/') 
        
        form = LoginForm()
        
        form_token = request.form.get('form_token')
        if form_token != session.get('form_token'):
            flash("This form has already been submitted.", "error")
            return redirect(url_for('register_user')) 


        if form.validate_on_submit():
            # Retrieve the user by username
            user = User.query.filter_by(USR_email=form.email.data).first()
            if user and user.check_password(form.password.data):
                if login_user(user, remember=form.remember_me.data):
                    session.permanent = not form.remember_me.data
                    flash('¡Inicio de sesión exitoso!', 'success')
                    session['remember_me'] = form.remember_me.data
                    
                    session.pop('form_token', None)

                    return redirect(request.args.get('next') or '/') 
                else:
                    flash('¡Este usuario está deshabilitado!', 'error')
            else:
                flash('¡Contraseña incorrecta!', 'error')


        # Return the form with error messages
        return render_template('auth/login.html',
                               title='Sign In',
                               form=form)
