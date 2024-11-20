from flask import Blueprint

from app.blueprints.select_packages_to_deliver.select_packages_to_deliver import SelectPackagesToDeliverView

select_packages_to_deliver = Blueprint(
    "select_packages_to_deliver", __name__, template_folder="templates/select_packages_to_deliver"
)
select_packages_to_deliver.add_url_rule(
    "/seleccionar_paquetes_a_entregar", view_func=SelectPackagesToDeliverView.as_view("select_packages_to_deliver")
)

class View:
    def get_blueprint(self):
        return select_packages_to_deliver

