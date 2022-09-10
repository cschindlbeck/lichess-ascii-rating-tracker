#!/usr/local/bin/python3
import berserk
import asciichartpy

API_TOKEN = "lip_oWEJVloOyWGv5eY16PTw"
#rating_type = 'Bullet'
rating_type = 'Puzzles'

def ascii():
    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)

    user_id = client.account.get()['id']

    # puz = client.users.get_puzzle_activity(max=1)
    # for ley in puz:
    #     print(ley)

    rating_history = client.users.get_rating_history(user_id)

    for rating in rating_history:
        if rating['name'] == rating_type:
            print(rating['name'])
            puzzle_rating = rating
            break

    rating_points = puzzle_rating['points']

    ratings = []
    for i in range(0,len(rating_points)):
        ratings.append(rating_points[i][3])

    config = {'height': 9, 'format': '{:8.0f}'}
    print(asciichartpy.plot(ratings, config))


def main():
    ascii()

if __name__ == "__main__":
    main()