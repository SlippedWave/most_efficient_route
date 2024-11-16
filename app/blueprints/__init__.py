ENABLED_VIEWS = [
    'app.blueprints.auth',
    'app.blueprints.manage_users',
    'app.blueprints.home',
    'app.blueprints.manage_packages',
    'app.blueprints.edit_user_info',
]

def register_blueprints(app):
    for view in ENABLED_VIEWS:
        klass = __import__(view, fromlist=['View'])
        v = klass.View()
        app.register_blueprint(v.get_blueprint())