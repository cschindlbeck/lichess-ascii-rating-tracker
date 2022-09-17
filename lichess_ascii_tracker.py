#!/usr/local/bin/python3
"""
Lichess ASCII rating tracker

Author: Chris Schindlbeck
License: MIT
"""

import os
import berserk  # pylint: disable=import-error
import asciichartpy  # pylint: disable=import-error


def get_ratings_from_lichess(api_token: str = None, rating_type: str = None) -> list:
    """
    Returns list of ratings from lichess using berserk

    :return: list of ratings from lichess
    :rtype: list
    """
    if api_token is None:
        raise Exception("api_token must be passed")
    if rating_type is None:
        raise Exception("rating_type must be passed")

    session = berserk.TokenSession(api_token)
    client = berserk.Client(session=session)
    user_id = client.account.get()['id']
    print("  ")
    print(f"{user_id}")
    rating_history = client.users.get_rating_history(user_id)

    # Get puzzle type and check for availability
    puzzle_type = rating_type
    puzzle_types = [d['name'] for d in rating_history if 'name' in d]
    if puzzle_type not in puzzle_types:
        raise Exception(f"Puzzle type is not valid, you chose {puzzle_type}. "
                        f"Please use one of these: {puzzle_types}")
    print(f"{puzzle_type}")

    puzzle_rating_points = [d['points'] for d in rating_history if d['name'] == puzzle_type][0]
    ratings = [row[3] for row in puzzle_rating_points]
    return ratings

def result_from_ascii(ratings: list) -> str:
    """
    Prints ASCII tracker given a list of ratings using asciichartpy

    :param ratings: List of ratings to be printed
    :type ratings: list
    """
    config = {'height': 9, 'format': '{:8.0f}'}
    result = asciichartpy.plot(ratings, config)

    return result

def print_to_markdown(text: str) -> None:
    """
    Prints text with decorator for HTML/Markdown

    :param ratings: String to be printed to HTML/Markdown
    :type ratings: list
    """
    print("<pre>")
    print("<code>")
    print(text)
    print("</code>")
    print("</pre>")

def get_token_from_env() -> str:
    """
    Api token from env variable

    :return: Api token from env variable
    :rtype: str
    """
    try:
        api_token = os.environ['API_TOKEN']
    except KeyError as keyerr:
        raise Exception(f"Environment variable {keyerr} does not exist") from keyerr

    return api_token

def get_rating_type_from_env() -> str:
    """
    Rating type from env variable

    :return: Rating type from env variable
    :rtype: str
    """
    try:
        rating_type = os.environ['RATING_TYPE']
    except KeyError as keyerr:
        raise Exception(f"Environment variable {keyerr} does not exist") from keyerr

    return rating_type

def main():
    """
    Main function
    """
    api_token=get_token_from_env()
    rating_type=get_rating_type_from_env()
    list_of_ratings = get_ratings_from_lichess(api_token, rating_type)
    result = result_from_ascii(list_of_ratings)
    print_to_markdown(result)


if __name__ == "__main__":
    main()
