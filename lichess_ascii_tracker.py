#!/usr/local/bin/python3
import berserk
import asciichartpy

API_TOKEN = "lip_oWEJVloOyWGv5eY16PTw"
#rating_type = 'Bullet'
rating_type = 'Puzzles'

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

    puzzle_names = [d['name'] for d in rating_history if 'name' in d]
    puzzle_type = 'Bullet'
    puzzle_rating_points = [d['points'] for d in rating_history if d['name'] == puzzle_type][0]

    ratings = []
    for i in range(0,len(puzzle_rating_points)):
        ratings.append(puzzle_rating_points[i][3])
    
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
