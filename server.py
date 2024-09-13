from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    maps_api_key = os.getenv('MAPS_API_KEY')
    return render_template(
        'index.html',
        MAPS_API_KEY = maps_api_key
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
