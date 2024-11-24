from flask import render_template, request, redirect, url_for, flash, jsonify
from dataclasses import dataclass

from flask.views import MethodView
from flask_login import current_user
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import and_
from datetime import datetime
import os

from app.models import Package
from app.extensions.database import db


def get_packages_to_deliver():
    return (
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
            joinedload(Package.status),
        )
        .filter(
            and_(
                Package.PCK_USR_assigned_to == current_user.USR_userId,
                Package.PCK_ST_statusId == 2,
            )
        )
        .all()
    )


def get_unique_addresses_list(packages_to_deliver):
    unique_addresses = {}
    for package in packages_to_deliver:
        address = str(package.address)
        if address not in unique_addresses:
            unique_addresses[address] = {
                "address": address,
                "packages": [],
                "address_id": package.PCK_ADD_addressId,
            }

        unique_addresses[address]["packages"].append(
            {
                "PCK_packageId": package.PCK_packageId,
                "PCK_client_name": package.PCK_client_name,
                "PCK_client_phone_num": package.PCK_client_phone_num,
                "PCK_delivery_date": package.PCK_delivery_date,
                "PCK_last_modified": package.PCK_last_modified,
                "PCK_special_delivery_instructions": package.PCK_special_delivery_instructions,
                "status": package.status.ST_value
            }
        )

    return list(unique_addresses.values())


class GetMostEfficentRouteView(MethodView):
    def get(self):

        packages_to_deliver = get_packages_to_deliver()
        unique_addresses = get_unique_addresses_list(packages_to_deliver)

        return render_template(
            "get_most_efficient_route/get_most_efficient_route.html",
            packages_to_deliver=packages_to_deliver,
            unique_addresses=unique_addresses,
            GOOGLE_MAPS_API_KEY=os.environ.get("GOOGLE_MAPS_API_KEY"),
        )

    def post(self):

        packageId = request.form.get("packageId")
        status = request.form.get("status")

        package = Package.query.get_or_404(packageId)

        package.PCK_ST_statusId = status
        package.PCK_delivery_date = datetime.now().date()

        try:
            db.session.commit()
            flash("¡Cambios registrados exitosamente!", "success")
        except Exception as e:
            flash("Error en la actualización de la información.", "error")

        packages_to_deliver = get_packages_to_deliver()
        unique_addresses = get_unique_addresses_list(packages_to_deliver)

        return jsonify(
            {
                "packages_to_deliver": [
                    {
                        "PCK_packageId": package.PCK_packageId,
                        "PCK_client_name": package.PCK_client_name,
                        "PCK_client_phone_num": package.PCK_client_phone_num,
                        "PCK_delivery_date": package.PCK_delivery_date.isoformat(),
                        "PCK_last_modified": package.PCK_last_modified.isoformat(),
                        "PCK_special_delivery_instructions": package.PCK_special_delivery_instructions,
                        "status": package.status.ST_value,
                    }
                    for package in packages_to_deliver
                ],
                "unique_addresses": unique_addresses,
            }
        )
