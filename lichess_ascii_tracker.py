#!/usr/local/bin/python3
import berserk
import asciichartpy

API_TOKEN = "lip_oWEJVloOyWGv5eY16PTw"
RATING_TYPE = 'Puzzles'

def get_ratings_from_lichess() -> list:
    """
    Returns list of ratings from lichess using berserk

    :return: list of ratings from lichess
    :rtype: list
    """
    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)
    user_id = client.account.get()['id']
    rating_history = client.users.get_rating_history(user_id)

    puzzle_types = [d['name'] for d in rating_history if 'name' in d]

    puzzle_type = RATING_TYPE
    if puzzle_type not in puzzle_types:
        raise Exception(f"Puzzle type is not valid, you chose {puzzle_type}! Please use one of these: {puzzle_types}")

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


def main():
    list_of_ratings = get_ratings_from_lichess()
    print_ascii_tracker(list_of_ratings)

if __name__ == "__main__":
    main()
