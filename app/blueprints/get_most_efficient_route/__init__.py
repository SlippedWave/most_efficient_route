from flask import Blueprint

from app.blueprints.get_most_efficient_route.get_most_efficient_route import (
    GetMostEfficentRouteView,
)

get_most_efficient_route = Blueprint(
    "get_most_efficient_route", __name__, template_folder="templates/get_most_efficient_route"
)
get_most_efficient_route.add_url_rule(
    "/ver_mi_ruta_de_entrega", view_func=GetMostEfficentRouteView.as_view("get_most_efficient_route")
)

class View: 
    def get_blueprint(self):
        return get_most_efficient_route;