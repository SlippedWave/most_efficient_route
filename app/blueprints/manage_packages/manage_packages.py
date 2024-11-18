from flask import render_template
from flask.views import MethodView
from sqlalchemy.orm import load_only, joinedload
from app.models import Package, Address, Status, User
from app.extensions.auth import require, has_permit_type


class ManagePackagesView(MethodView):
    @require(lambda: has_permit_type("Administrador", "Almacenista"))
    def get(self):
        drivers = (
            User.query.with_entities(
                User.USR_userId, User.USR_telephone, User.USR_name, User.USR_last_name
            )
            .filter_by(USR_PER_permitId=3)
            .all()
        )
        addresses = Address.query.with_entities(
            Address.ADD_addressId,
            Address.ADD_street,
            Address.ADD_ext_number,
            Address.ADD_int_number,
            Address.ADD_neighborhood,
            Address.ADD_zip_code,
            Address.ADD_city,
            Address.ADD_state,
        ).all()

        packages = Package.query.options(
            load_only(
                Package.PCK_packageId,
                Package.PCK_client_name,
                Package.PCK_client_phone_num,
                Package.PCK_delivery_date,
                Package.PCK_last_modified,
            ),
            joinedload(Package.address),
            joinedload(Package.assigned_to_user),
            joinedload(Package.status).load_only(Status.ST_value),
        ).all()
        
        return render_template(
            "manage_packages/manage_packages.html",
            packages=packages,
            drivers=drivers,
            addresses=addresses,
        )
