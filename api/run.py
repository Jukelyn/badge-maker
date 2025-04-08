# pylint: disable=E0401
"""
Initilizes the flask app.
"""
from flask import Flask
from flask_cors import CORS
from src.routes import register_routes

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000",
     "https://badge-maker.jukelyn.com/"])

register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
