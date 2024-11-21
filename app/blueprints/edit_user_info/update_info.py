from flask import render_template, jsonify, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import current_user
from datetime import datetime

from app.models import User
from app.blueprints.edit_user_info.edit_user_info_form import EditUserInfoForm
from app.extensions.database import db

class UpdateInfoView(MethodView):
    def get(self):
        form = EditUserInfoForm(
            USR_telephone=current_user.USR_telephone,
            USR_address=current_user.USR_address
        )
        
        return render_template(
            "edit_user_info/edit_user_info.html",
            form=form,
            current_user=current_user 
        )
        
    def post(self):
        user = User.query.get_or_404(current_user.USR_userId)
        form = EditUserInfoForm(request.form, obj=user)

        if form.validate_on_submit():
            user.USR_telephone = form.USR_telephone.data
            user.USR_address = form.USR_address.data
            user.USR_last_modified = datetime.now()
            user.USR_modified_by = current_user.USR_userId

            if form.plain_password.data:
                user.set_password(form.plain_password.data)

            try:
                db.session.commit()
                flash("¡Cambios realizados exitosamente!", "success")
                return redirect(url_for("edit_user_info.edit_user_info"))  
            except Exception as e:
                print(f"Error updating user: {e}")
                return jsonify(
                    {"status": "error", "message": "Error al actualizar el usuario"}
                )
        else:
            return render_template(
                "edit_user_info/edit_user_info.html",
                form=form,
                current_user=current_user,
                errors=form.errors
            )
