from flask import render_template, flash, redirect, url_for
from flask.views import MethodView

from app.models import User, Status, Permit
from app.blueprints.manage_users.register_user_form import RegisterUserForm
from app.extensions.auth import require, has_permit_type

class ManageUsersView(MethodView):
    @require(lambda: has_permit_type("Administrador"))
    def get(self):
        