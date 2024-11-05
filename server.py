from flask import Flask, render_template
from extensions import connect_with_connector
import os

def create_app():
    app = Flask(__name__)
    
    pool = connect_with_connector()
    
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
            with pool.connect() as conn:
                result = conn.execute("SELECT 1") 
                rows = [row for row in result]
            return f"Connection successful! Query result: {rows}"
        except Exception as e:
            return f"An error occurred: {e}", 500
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8001, debug=True)
