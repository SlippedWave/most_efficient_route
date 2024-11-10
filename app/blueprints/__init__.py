ENABLED_VIEWS = [
    'app.blueprints.auth',
    'app.blueprints.register_user',
    'app.blueprints.home',
]

def register_blueprints(app):
    for view in ENABLED_VIEWS:
        klass = __import__(view, fromlist=['View'])
        v = klass.View()
        app.register_blueprint(v.get_blueprint())