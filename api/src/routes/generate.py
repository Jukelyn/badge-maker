"""
This module provides the route for the generation endpoint.
"""
from flask import request, jsonify
from simplepycons import all_icons
from simplepycons.base_icon import Icon


def get_badge_url(icon: Icon) -> str:
    """
    Generates the markdown badge URL.

    Args:
        icon (Icon): Simplepyicons icon.

    Returns:
        (str): The markdown badge URL.
    """
    icon_slug = icon.name
    hex_code = icon.primary_color[1:]
    # print(icon_slug)
    base_url = "https://img.shields.io/badge"

    first_part = f"![{icon_slug.title()}]"

    queries = f"style=for-the-badge&logo={icon_slug}&logoColor=white"

    link_part = f"({base_url}/{icon_slug}-%23{hex_code}.svg?{queries})"
    badge_url = first_part + link_part

    return badge_url


def make_md_table_row(icon: Icon) -> dict:
    """
    Makes a dictionary representing a markdown table row for the badge.

    Args:
        icon (Icon): Simplepyicons icon.

    Returns:
        (dict): A dictionary containing the table row data.
    """
    link = get_badge_url(icon)

    return {
        "name": icon.name.title(),
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
        data: dict[str, list[str]] = request.get_json()

        if (
            not data or
            'slugs' not in data or
            not isinstance(data['slugs'], list)
        ):
            msg = " Please provide a list of 'slugs' in the JSON body."
            return jsonify({"error": "Invalid request." + msg}), 400

        slugs = {slug for slug in data['slugs'] if slug.strip()}
        results = []
        invalid_slugs = []

        for slug in slugs:
            try:
                icon_factory = all_icons.__dict__[f"get_{slug}_icon"]
            except KeyError:
                invalid_slugs.append(slug)
                continue

            icon = icon_factory()
            results.append(make_md_table_row(icon))

        response_data = {
            "badges": results,
            "invalid_slugs": invalid_slugs
        }

        return jsonify(response_data)
