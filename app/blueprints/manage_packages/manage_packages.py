from flask import render_template
from flask.views import MethodView
from sqlalchemy.orm import load_only, joinedload
from app.models import User, Package, Status
from app.extensions.auth import require, has_permit_type

class ManagePackagesView(MethodView):
    @require(lambda: has_permit_type("Administrador"))
    def get(self):
        packages = Package.query.options(
            load_only(
                Package.PCK_packageId,
                Package.PCK_client_name,
                Package.PCK_delivery_date,
                Package.PCK_last_modified
            ),
            joinedload(Package.assigned_to_user), 
            joinedload(Package.address),  
            joinedload(Package.status).load_only(Status.ST_value)
        ).all()
        return render_template("manage_packages/manage_packages.html", packages=packages)
