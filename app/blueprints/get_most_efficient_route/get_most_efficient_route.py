from flask import render_template, jsonify, redirect, url_for
from dataclasses import dataclass

from flask.views import MethodView
from flask_login import current_user
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import and_
from datetime import datetime
import os

from app.models import Package, Address
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

        unique_addresses = (
            db.session.query(Address)
            .join(Package, Package.PCK_ADD_addressId == Address.ADD_addressId)
            .filter(
                and_(
                    Package.PCK_USR_assigned_to == current_user.USR_userId,
                    Package.PCK_ST_statusId == 2,  # Filter by package status
                )
            )
            .distinct()
            .all()
        )


        return render_template(
            "get_most_efficient_route/get_most_efficient_route.html",
            packages_to_deliver=packages_to_deliver,
            unique_addresses=[{"address": str(address)} for address in unique_addresses],
            GOOGLE_MAPS_API_KEY=os.environ.get('GOOGLE_MAPS_API_KEY'),
        )


    def post(self):

        return redirect(url_for("get_most_efficient_route.get_most_efficient_route"))
