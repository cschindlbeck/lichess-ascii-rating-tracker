"""
Unit tests for lichess_ascii_tracker
"""

import os
import unittest
from unittest.mock import patch

from lichess_ascii_tracker import LichessChartGenerator, _result_from_ascii


class TestLichessChartGenerator(unittest.TestCase):
    """
    Test class for LichessChartGenerator
    """

    def setUp(self):
        """
        Set up for tests
        """
        os.environ["API_TOKEN"] = "test_token"

    @patch("berserk.Client")
    def test_run(self, mock_client):
        """
        Test the run method
        """
        mock_client.return_value.account.get.return_value = {"id": "test_user"}
        mock_client.return_value.users.get_rating_history.return_value = [
            {
                "name": "Bullet",
                "points": [
                    [2023, 1, 1, 1500],
                    [2023, 1, 2, 1550],
                    [2023, 1, 3, 1525],
                ],
            }
        ]

        generator = LichessChartGenerator("Bullet")
        generator.client = mock_client.return_value
        # suppress print
        with patch("builtins.print"):
            generator.run()

        mock_client.return_value.account.get.assert_called_once()
        mock_client.return_value.users.get_rating_history.assert_called_once_with("test_user")

    def test_result_from_ascii(self):
        """
        Test the _result_from_ascii method
        """
        ratings = [1500, 1550, 1525]
        result = _result_from_ascii(ratings)
        self.assertIsInstance(result, str)
        self.assertIn("1550", result)
        self.assertIn("1500", result)

    @patch("berserk.Client")
    def test_get_ratings_from_lichess(self, mock_client):
        """
        Test the get_ratings_from_lichess method
        """
        mock_client.return_value.account.get.return_value = {"id": "test_user"}
        mock_client.return_value.users.get_rating_history.return_value = [
            {
                "name": "Bullet",
                "points": [
                    [2023, 1, 1, 1500],
                    [2023, 1, 2, 1550],
                    [2023, 1, 3, 1525],
                ],
            }
        ]

        generator = LichessChartGenerator("Bullet")
        generator.client = mock_client.return_value
        user_id, ratings = generator.get_ratings_from_lichess()

        self.assertEqual(user_id, "test_user")
        self.assertEqual(ratings, [1500, 1550, 1525])

    @patch("berserk.Client")
    def test_invalid_rating_type(self, mock_client):
        """
        Test invalid rating type
        """
        mock_client.return_value.account.get.return_value = {"id": "test_user"}
        mock_client.return_value.users.get_rating_history.return_value = [{"name": "Bullet", "points": []}]

        generator = LichessChartGenerator("Blitz")
        generator.client = mock_client.return_value
        with self.assertRaises(IndexError):
            generator.get_ratings_from_lichess()


if __name__ == "__main__":
    unittest.main()
