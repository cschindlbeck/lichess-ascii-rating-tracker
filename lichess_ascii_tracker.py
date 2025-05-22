#!/usr/local/bin/python3
"""
Lichess ASCII chart generator

Author: Chris Schindlbeck
License: MIT
"""

import argparse
import os
from datetime import datetime

import asciichartpy  # type: ignore
import berserk  # type: ignore

HSIZE = 60


def _result_from_ascii(ratings: list) -> str:
    """
    Returns string of ASCII given a list of ratings using asciichartpy

    :param ratings: List of ratings to be printed
    :type ratings: list
    :return: String of asciichart plot from ratings
    :rtype: str
    """
    config = {"height": 9, "format": "{:8.0f}"}
    result = asciichartpy.plot(ratings, config)

    return result


class LichessChartGenerator:
    """
    Class to generate ascii chart of lichess ratings
    """

    def __init__(self, rating_type=None):
        if rating_type is None:
            raise TypeError("rating_type must be set")

        # check if rating type is in valid dict of ratings
        self.rating_type = rating_type

        try:
            api_token = os.environ["API_TOKEN"]
        except KeyError as keyerr:
            raise KeyError(f"API_TOKEN must be passed, environment variable {keyerr} does not exist") from keyerr

        # put try catch in case of invalid token
        session = berserk.TokenSession(api_token)
        self.client = berserk.Client(session=session)

    def run(self):
        """
        Main function to generate ascii chart
        """
        user_id, list_of_ratings = self.get_ratings_from_lichess()
        result = _result_from_ascii(list_of_ratings)
        self.print_to_markdown(user_id, result)

    def get_ratings_from_lichess(self) -> tuple:
        """
        Returns list of ratings from lichess using berserk

        :return: tuple of user_id and ratings from lichess
        :rtype: tuple
        """

        user_id = self.client.account.get()["id"]
        rating_history = self.client.users.get_rating_history(user_id)

        # Get puzzle type and check for availability
        puzzle_type = self.rating_type
        puzzle_types = [d["name"] for d in rating_history if "name" in d]
        if puzzle_type not in puzzle_types:
            raise IndexError(f"Puzzle type is not valid, you chose {puzzle_type}. Please use one of these: {puzzle_types}")

        prp = [d["points"] for d in rating_history if d["name"] == puzzle_type]
        puzzle_rating_points = prp[0]
        ratings = [row[3] for row in puzzle_rating_points]

        if len(ratings) == 0:
            raise ValueError("Puzzle type never played")

        # reduce list len to fit screen
        if len(ratings) >= HSIZE:
            step = int(len(ratings) / HSIZE)
            ratings = ratings[0 : len(ratings) : step]

        return (user_id, ratings)

    def print_to_markdown(self, user_name: str, rating: str) -> None:
        """
        Prints text with decorator for HTML/Markdown

        :param user_name: String of user_name
        :type user_name: str
        :param text: ratings
        :type text: str
        """

        print(
            r"""
          _      _      _
         | |    (_)    | |
         | |     _  ___| |__   ___  ___ ___
         | |    | |/ __| '_ \ / _ \/ __/ __|
         | |____| | (__| | | |  __/\__ \__ \
         |______|_|\___|_| |_|\___||___/___/"""
        )
        print("")
        print(rating)
        print("")
        # dd/mm/YY H:M:S
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
        print(f"User: {user_name}, Rating type: {self.rating_type} on lichess.org")
        print(f"Last update: {dt_string}")


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description="Generate Lichess charts based on rating type.")
    parser.add_argument(
        "-r",
        "--rating_type",
        type=str,
        required=True,
        help="Specify the rating type (e.g., Blitz, Bullet, etc.)",
    )

    args = parser.parse_args()

    rating_type = args.rating_type
    lichess_chart_generator = LichessChartGenerator(rating_type)
    lichess_chart_generator.run()


if __name__ == "__main__":
    main()
