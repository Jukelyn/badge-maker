# pylint: disable=E0401
"""
This module provides the route for the generation endpoint.
"""
from flask import request, jsonify
from simpleicons.all import icons


def get_badge_url(name: str) -> str:
    """
    Generates the markdown badge URL.

    Args:
        name (str): The slug of the badge from simpleicons.

    Returns:
        (str): The markdown badge URL.
    """
    base_url = "https://img.shields.io/badge"
    queries = f"?style=for-the-badge&logo={name}&logoColor=white"
    first_part = f"![{name.title()}]"
    link_part = f"({base_url}/{name}-%23<badge_color>.svg{queries})"
    badge_url = first_part + link_part
    return badge_url


def make_md_table_row(name: str) -> dict:
    """
    Makes a dictionary representing a markdown table row for the badge.

    Args:
        name (str): The slug of the badge from simpleicons.

    Returns:
        (dict): A dictionary containing the table row data.
    """
    link = get_badge_url(name)
    return {
        "name": name.title(),
        "markdown": link,
        "markdown_code": f"`{link}`"
    }


def generate_route(app):
    """
    Registers the generate endpoint of the application.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.route('/generate_badges', methods=['POST'])
    def generate_badges():
        """
        The endpoint to generate markdown badges for a list of simple-icons
        slugs.

        Returns:
            (jsonify): A JSON response containing a list of badge details.
        """
        data = request.get_json()
        if (
            not data or
            'slugs' not in data or
            not isinstance(data['slugs'], list)
        ):
            msg = " Please provide a list of 'slugs' in the JSON body."
            return jsonify({"error": "Invalid request." + msg}), 400

        slugs = data['slugs']
        results = []
        invalid_slugs = []

        for slug in slugs:
            icon = icons.get(slug)
            if icon:
                results.append(make_md_table_row(icon.slug))
            else:
                invalid_slugs.append(slug)

        response_data = {
            "badges": results,
            "invalid_slugs": invalid_slugs
        }

        return jsonify(response_data)
