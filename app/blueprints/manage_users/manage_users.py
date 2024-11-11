from flask import render_template, flash, redirect, url_for
from flask.views import MethodView
from sqlalchemy.orm import load_only, joinedload
from app.models import User, Permit, Status
from app.extensions.auth import require, has_permit_type


class ManageUsersView(MethodView):
    @require(lambda: has_permit_type("Administrador"))
    def get(self):
        users = User.query.options(
            load_only(
                User.USR_userId,
                User.USR_name,
                User.USR_last_name,
                User.USR_email,
                User.USR_telephone,
                User.USR_last_modified,
            ),
            joinedload(User.permit).load_only(
                Permit.PMT_type  # Use class-bound attribute, not string
            ), 
            joinedload(User.status).load_only(
                Status.ST_value  # Use class-bound attribute, not string
            ), 
        ).all()
        return render_template("manage_users/manage_users.html", users=users)
