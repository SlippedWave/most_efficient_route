from flask import Flask, render_template
from app.extensions.database import db, uri, get_db_session
from flask_migrate import Migrate
from sqlalchemy import text
import os
from dotenv import load_dotenv


migrate = Migrate() 

def create_app():
    app = Flask (__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = uri.render_as_string(hide_password=False)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

    db.init_app(app) 
    from app.models import User, Permit, Package, Status 
    
    migrate.init_app(app, db)
    
    @app.route('/') 
    @app.route('/index')
    def index():
        maps_api_key = os.environ.get('MAPS_API_KEY')
        return render_template(
            'index.html',
            MAPS_API_KEY=maps_api_key
        )
        
    
        
    @app.route('/test-connection')
    @app.route('/test-connection')
    def test_connection():
        try:
            # Get a session from the database
            session = get_db_session()  # Get a new session

            # Query the permits table to get all records
            permits = session.query(Permit).all()  # This will use SQLAlchemy ORM

            # If there are permits, return their names (or any field you need)
            if permits:
                permit_names = [permit.name for permit in permits]  # Adjust to the actual field name in Permit
                return f"Connection successful! Permit names: {permit_names}"
            else:
                return "No permits found in the database."
        except Exception as e:
            return f"An error occurred: {e}", 500
        
        finally:
            # Ensure that the session is closed after the query
            session.close()
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8001, debug=True)
