#!/usr/local/bin/python3

import os
import berserk
import asciichartpy


def get_ratings_from_lichess(API_TOKEN: str = None, RATING_TYPE: str = None) -> list:
    """
    Returns list of ratings from lichess using berserk

    :return: list of ratings from lichess
    :rtype: list
    """
    if API_TOKEN is None: 
        raise Exception("API_TOKEN must be passed")
    if RATING_TYPE is None: 
        raise Exception("RATING_TYPE must be passed")

    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)
    user_id = client.account.get()['id']
    print(f"{user_id}")
    rating_history = client.users.get_rating_history(user_id)

    # Get puzzle type and check for availability
    puzzle_type = RATING_TYPE
    puzzle_types = [d['name'] for d in rating_history if 'name' in d]
    if puzzle_type not in puzzle_types:
        raise Exception(f"Puzzle type is not valid, you chose {puzzle_type}. Please use one of these: {puzzle_types}")
    print(f"{puzzle_type}")

    puzzle_rating_points = [d['points'] for d in rating_history if d['name'] == puzzle_type][0]
    ratings = [row[3] for row in puzzle_rating_points]
    return ratings

def print_ascii_tracker(ratings: list) -> None:
    """
    Prints ASCII tracker given a list of ratings using asciichartpy

    :param ratings: List of ratings to be printed
    :type ratings: list
    """
    config = {'height': 9, 'format': '{:8.0f}'}
    print(asciichartpy.plot(ratings, config))

def get_token_from_env():
    try:
        API_TOKEN = os.environ['API_TOKEN']
    except KeyError as keyerr:
        raise Exception(f"Environment variable {keyerr} does not exist") from keyerr

    return API_TOKEN

def get_rating_type_from_env():
    try:
        RATING_TYPE = os.environ['RATING_TYPE']
    except KeyError as keyerr:
        raise Exception(f"Environment variable {keyerr} does not exist") from keyerr

    return RATING_TYPE

def main():
    API_TOKEN=get_token_from_env()
    RATING_TYPE=get_rating_type_from_env()
    list_of_ratings = get_ratings_from_lichess(API_TOKEN, RATING_TYPE)
    print_ascii_tracker(list_of_ratings)


if __name__ == "__main__":
    main()
