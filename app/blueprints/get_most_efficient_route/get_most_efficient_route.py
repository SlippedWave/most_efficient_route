from flask import render_template, flash, redirect, url_for
from flask.views import MethodView
from flask_login import current_user
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import and_
from datetime import datetime

from app.models import Package
from app.extensions.database import db


class GetMostEfficentRouteView(MethodView):
    def get(self):
        packages_to_deliver = (
            Package.query.options(
                load_only(
                    Package.PCK_packageId,
                    Package.PCK_client_name,
                    Package.PCK_client_phone_num,
                    Package.PCK_delivery_date,
                    Package.PCK_last_modified,
                    Package.PCK_special_delivery_instructions,
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
            "get_most_efficient_route/get_most_efficient_route.html",
            packages_to_deliver=packages_to_deliver,
        )

    def post(self):

        return redirect(url_for("get_most_efficient_route.get_most_efficient_route"))
