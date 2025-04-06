# pylint: disable=E0401
"""
This module provides the route for the index page.
"""
from flask import render_template


def index_route(app):
    """
    Registers the main entry point of the application.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.route("/", methods=["GET"])
    def index():
        """
        Handles requests to the main `/` route.
        """
        return render_template("index.html")
