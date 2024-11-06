from flask import Flask, render_template
from .extensions.database import db, uri
from flask_migrate import Migrate
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

migrate = Migrate() 

def create_app():
    app = Flask (__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = uri.render_as_string(hide_password=False)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

    db.init_app(app) 
    
    from .models import User, Permit, Package, Status 
    
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
    def test_connection():
        try:
            # Connect using SQLAlchemy's connection pooling
            with db.session.connection() as conn:
                # Execute the query to fetch table names
                result = conn.execute(text("DESCRIBE users"))
                
                # Collect the table names from the result set
                rows = [row[0] for row in result.fetchall()]  # result.fetchall() retrieves all rows
                
            return f"Connection successful! Table names: {rows}"
        except Exception as e:
            return f"An error occurred: {e}", 500

        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8001, debug=True)
