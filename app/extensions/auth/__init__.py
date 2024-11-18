from functools import update_wrapper

from flask import current_app, abort, url_for
from flask_login import current_user


def get_pages_by_role():
    return {
        "Administrador": [
            {"name": "Usuarios", "url": url_for("manage_users.manage_users")},
            {"name": "Paquetes", "url": url_for("manage_packages.manage_packages")},
        ],
        "Almacenista": [
            {"name": "Paquetes", "url": url_for("manage_packages.manage_packages")},
        ],
        "Repartidor": [
            {"name": "Mis paquetes", "url": ""},
            {"name": "Mi ruta", "url": ""},
        ],
    }
    
def authorized(checker):
    """Check if current user is authenticated and authorized.

    Meant to be used inside views and templates to protect part of resources.
    """
    return current_user.is_authenticated and checker()


def require(checker):
    """
    Ensure that current user is authenticated and authorized to access the
    decorated view.  For example::

        @app.route('/protected')
        @require(Any(is_user('id'), HasPermitType('admins')))
        def protected():
            pass

    """

    def decorator(fn):
        def wrapped_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if not checker():
                abort(403)
            return fn(*args, **kwargs)

        return update_wrapper(wrapped_function, fn)

    return decorator


class has_permit_type(object):
    """Check if the current user's permit matches any of the provided permit types."""

    def __init__(self, *permit_types):
        self.permit_types = set(permit_types)

    def __call__(self):
        user_permit_type = current_user.get_permit()
        # Check if the user's permit type is in the specified permit types
        return user_permit_type and user_permit_type in self.permit_types
