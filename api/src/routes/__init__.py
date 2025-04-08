"""
Initializes the routes.
"""
from .generate import generate_route
from .health import health_route
from .available_icons import available_icons_route


def register_routes(app):
    """
    Register routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    Routes:
        routes.index: Renders the main page.
        routes.health: Healthcheck endpoint.
    """

    generate_route(app)
    available_icons_route(app)
    health_route(app)
