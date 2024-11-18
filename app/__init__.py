from flask import Flask, render_template
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from app.blueprints import register_blueprints
from flask_login import LoginManager, current_user
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

from app.extensions.auth import authorized, get_pages_by_role
from app.extensions.database import db, uri

load_dotenv()

app = Flask(__name__)

# Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = uri.render_as_string(hide_password=False)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# TO KEEP THE BLOODY PYTHON FROM GENERATIONG DUMB ASS CACHE FILES
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["DEBUG"] = True


# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
app.jinja_env.globals["authorized"] = authorized
migrate = Migrate(app, db)

from app.models import *

# Enable debug toolbar only in debug mode
if app.debug:
    DebugToolbarExtension(app)

# Register blueprints
register_blueprints(app)


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.context_processor
def inject_pages():
    if current_user.is_authenticated:
        user_role = current_user.get_permit()
        pages = get_pages_by_role().get(user_role, [])
    else:
        pages = []
    return {"nav_pages": pages}


# Logging configuration (only for production mode)
if not app.debug:
    file_handler = RotatingFileHandler(
        "tmp/app.log", maxBytes=1 * 1024 * 1024, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("Application startup")

if __name__ == "__main__":
    app.run()
