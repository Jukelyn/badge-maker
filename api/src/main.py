# pylint: disable=E0401
"""
A script to generate markdown badges for Ileriayo/markdown-badges using icons
from simple-icons/simple-icons
"""
from simpleicons.all import icons

LINKS: list[str] = []


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

    global LINKS  # pylint: disable=W0602
    LINKS.append(badge_url)

    return badge_url


def make_md(name: str) -> str:
    """
    Makes a markdown style output to add the badge to a table.

    Args:
        name (str): The slug of the badge from simpleicons.

    Returns:
        (str): The styled output for the badge.
    """

    link = get_badge_url(name)  # pylint: disable=W0621

    return f"| {name.title()} | {link} | `{link}` |"


def get_slugs() -> set[str]:
    """
    Makes a set of the slugs.

    Returns:
        (set[str]): The set containing the slugs.
    """

    slugs = set()

    print("Enter blank to stop inputting.\n")

    while True:
        slug = input("Enter the simpleicons icon slug: ")
        print()

        if not slug:
            break

        icon = icons.get(slug)

        if icon:
            slugs.add(icon.slug)
        else:
            print(f"\nIcon '{slug}' is not a valid simpleicons icon slug.\n")

    return slugs


if __name__ == "__main__":
    badges = get_slugs()

    print("\n--- Generated Badges (markdown table format) ---\n")

    for badge in badges:
        print(make_md(badge))

    print("\n--- Generated Links ---\n")

    for link in LINKS:
        print(link)
