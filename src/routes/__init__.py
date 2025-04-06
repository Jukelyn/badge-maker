"""
Initializes the routes.
"""
from .index import index_route
from .health import health_route


def register_routes(app):
    """
    Register routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    Routes:
        routes.index: Renders the main page.
        routes.health: Healthcheck endpoint.
    """

    index_route(app)
    health_route(app)
