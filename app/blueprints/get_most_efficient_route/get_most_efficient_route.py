from flask import render_template, jsonify, redirect, url_for
from dataclasses import dataclass

from flask.views import MethodView
from flask_login import current_user
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import and_
from datetime import datetime
import os

from app.models import Package

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

        unique_addresses = {}
        for package in packages_to_deliver:
            address = str(package.address)
            if address not in unique_addresses:
                unique_addresses[address] = {
                    "address": address,
                    "packages": [],
                    "address_id": package.PCK_ADD_addressId
                }

            unique_addresses[address]["packages"].append(
                {
                    "PCK_packageId": package.PCK_packageId,
                    "PCK_client_name": package.PCK_client_name,
                    "PCK_client_phone_num": package.PCK_client_phone_num,
                    "PCK_delivery_date": package.PCK_delivery_date,
                    "PCK_last_modified": package.PCK_last_modified,
                    "PCK_special_delivery_instructions": package.PCK_special_delivery_instructions,
                }
            )

        unique_addresses_list = list(unique_addresses.values())

        return render_template(
            "get_most_efficient_route/get_most_efficient_route.html",
            packages_to_deliver=packages_to_deliver,
            unique_addresses=unique_addresses_list,
            GOOGLE_MAPS_API_KEY=os.environ.get("GOOGLE_MAPS_API_KEY"),
        )

    def post(self):

        return redirect(url_for("get_most_efficient_route.get_most_efficient_route"))
