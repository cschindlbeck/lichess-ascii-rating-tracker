#!/usr/local/bin/python3
"""
Lichess ASCII chart generator

Author: Chris Schindlbeck
License: MIT
"""

import os
from datetime import datetime
import berserk  # pylint: disable=import-error
from berserk.exceptions import ResponseError
import asciichartpy  # pylint: disable=import-error

class LichessChartGenerator:
    """
    Class to generate ascii chart of lichess ratings

    """
    def __init__(self):

        try:
            api_token = os.environ['API_TOKEN']
        except KeyError as keyerr:
            raise Exception(f"API_TOKEN must be passed, environment variable"
                            f" {keyerr} does not exist") from keyerr

        # put try catch in case of invalid token
        try:
            session = berserk.TokenSession(api_token)
            self.client = berserk.Client(session=session)
            user_id2 = self.client.account.get()['id']
        except ResponseError as err:
            print(f"No such token {api_token}")

        try:
            self.rating_type = os.environ['RATING_TYPE']
        except KeyError as keyerr:
            raise Exception(f"RATING_TYPE must be passed, environment variable"
                            f" {keyerr} does not exist") from keyerr

    def run(self):
        """
        Main function to generate ascii chart
        """
        user_id, list_of_ratings = self.get_ratings_from_lichess()
        result = self.result_from_ascii(list_of_ratings)
        self.print_to_markdown(user_id, result)

    def get_ratings_from_lichess(self) -> tuple:
        """
        Returns list of ratings from lichess using berserk

        :return: tuple of user_id and ratings from lichess
        :rtype: tuple
        """

        user_id = self.client.account.get()['id']
        rating_history = self.client.users.get_rating_history(user_id)

        # Get puzzle type and check for availability
        puzzle_type = self.rating_type
        puzzle_types = [d['name'] for d in rating_history if 'name' in d]
        if puzzle_type not in puzzle_types:
            raise Exception(f"Puzzle type is not valid, you chose {puzzle_type}. "
                            f"Please use one of these: {puzzle_types}")

        puzzle_rating_points = [d['points'] for d in rating_history if d['name'] == puzzle_type][0]
        ratings = [row[3] for row in puzzle_rating_points]
        return (user_id, ratings)

    def result_from_ascii(self, ratings: list) -> str:
        """
        Prints ASCII tracker given a list of ratings using asciichartpy

        :param ratings: List of ratings to be printed
        :type ratings: list
        """
        config = {'height': 9, 'format': '{:8.0f}'}
        result = asciichartpy.plot(ratings, config)

        return result

    def print_to_markdown(self, text: str, text2: str) -> None:
        """
        Prints text with decorator for HTML/Markdown

        :param ratings: String to be printed to HTML/Markdown
        :type ratings: list
        """
        print("<pre>")
        print("<code>")
        print(f"User: {text}, Rating type: {self.rating_type} on lichess.org")
        print("")
        print(text2)
        print("")
        # dd/mm/YY H:M:S
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
        print(f"Last update: {dt_string}")
        print("</code>")
        print("</pre>")


def main():
    """
    Main function
    """
    lichess_chart_generator = LichessChartGenerator()
    lichess_chart_generator.run()


if __name__ == "__main__":
    main()
