from flask import Blueprint
from app.blueprints.manage_packages.register_package import RegisterUserView
from app.blueprints.manage_packages.manage_packages import ManagePackagesView
from app.blueprints.manage_packages.edit_package import EditPackageView

manage_packages = Blueprint(
    "manage_packages", __name__, template_folder="templates/manage_packages"
)
manage_packages.add_url_rule(
    "/administrar_paquetes", view_func=ManagePackagesView.as_view("manage_packages")
)
manage_packages.add_url_rule(
    "/registrar_paquete", view_func=RegisterUserView.as_view("register_package")
)
manage_packages.add_url_rule(
    "/editar_paquete/<int:id>", view_func=EditPackageView.as_view("edit_package")
)


class View:
    def get_blueprint(self):
        return manage_packages
