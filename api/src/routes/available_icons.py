# pylint: disable=E0401
"""
This module provides the route for the available icons endpoint.
"""
from flask import jsonify
from simplepycons import all_icons


def available_icons_route(app):
    """
    Registers the available icons endpoint of the application.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.route('/available_icons', methods=['GET'])
    def get_available_icons():
        """
        API endpoint to retrieve a list of all available simpleicons slugs.

        Returns:
            (jsonify): JSON response containing all simpleicons slugs.
        """

        return jsonify(list(all_icons.keys()))
