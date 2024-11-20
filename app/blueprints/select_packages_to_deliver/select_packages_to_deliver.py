from flask import render_template, flash, redirect, url_for
from flask.views import MethodView
from sqlalchemy.orm import load_only, joinedload
from flask_login import current_user
from sqlalchemy import and_


from app.models import Package, Status
from app.blueprints.select_packages_to_deliver.select_packages_to_deliver_form import (
    SelectPackagesToDeliverForm,
)


class SelectPackagesToDeliverView(MethodView):
    def get(self):

        form = SelectPackagesToDeliverForm()

        packages = (
            Package.query.options(
                load_only(
                    Package.PCK_packageId,
                    Package.PCK_client_name,
                    Package.PCK_client_phone_num,
                    Package.PCK_last_modified,
                ),
                joinedload(Package.address),
            )
            .filter(
                and_(
                    Package.PCK_USR_assigned_to == current_user.USR_userId,
                    Package.PCK_ST_statusId == 1,
                )
            )
            .all()
        )

        selected_packages = (
            Package.query.options(
                load_only(
                    Package.PCK_packageId,
                    Package.PCK_client_name,
                    Package.PCK_client_phone_num,
                    Package.PCK_delivery_date,
                    Package.PCK_last_modified,
                    Package.PCK_special_delivery_instructions
                ),
                joinedload(Package.address),
            )
            .filter(
                and_(
                    Package.PCK_USR_assigned_to == current_user.USR_userId,
                    Package.PCK_ST_statusId == 2,
                )
            )
            .all()
        )

        return render_template(
            "select_packages_to_deliver/select_packages_to_deliver.html",
            url=url_for("select_packages_to_deliver.select_packages_to_deliver"),
            form=form,
            packages=packages,
            selected_packages=selected_packages,
        )

    def post(self):

        form = SelectPackagesToDeliverForm()

        if form.validate_on_submit():
            
            return redirect(
                url_for("select_packages_to_deliver.select_packages_to_deliver")
            )
            
        return redirect(
            url_for("select_packages_to_deliver.select_packages_to_deliver")
        )
