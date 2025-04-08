# pylint: disable=E0401
"""
This module provides the route for the healthcheck endpoint.
"""
from flask import jsonify


def health_route(app):
    """
    Registers the healthcheck endpoint of the application.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Handles requests to the main `/health` route.
        """

        return jsonify({"status": "healthy"}), 200
