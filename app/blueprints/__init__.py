ENABLED_VIEWS = [
    'app.blueprints.auth',
    'app.blueprints.home',
    'app.blueprints.edit_user_info',
    'app.blueprints.manage_users',
    'app.blueprints.manage_packages',
    'app.blueprints.select_packages_to_deliver'
    # 'app.blueprints.get_most_efficient_route'
]

def register_blueprints(app):
    for view in ENABLED_VIEWS:
        klass = __import__(view, fromlist=['View'])
        v = klass.View()
        app.register_blueprint(v.get_blueprint())