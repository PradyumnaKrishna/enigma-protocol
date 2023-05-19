"""
Tests database module
"""

import datetime
import unittest

from database import DataBase


class TestDataBase(unittest.TestCase):
    """
    Test DataBase Class that runs SQLite query
    """

    def setUp(self):
        self.database = DataBase()

    def test_save_user(self):
        """
        Test insertion and selection query
        """
        public_key = "random-public-key"
        user_id = self.database.save_user(public_key)
        self.assertEqual(public_key, self.database.get_public_key(user_id))

    def test_get_user_cards(self):
        """
        Test retrieving user cards with timestamps
        """
        # Assuming the database already has some user cards
        user_cards = self.database.get_user_cards()

        for user_card in user_cards:
            # Check if the timestamp key exists in each user card
            self.assertIn("timestamp", user_card)

            # Check if the timestamp value is a valid datetime string
            try:
                datetime.strptime(user_card["timestamp"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                self.fail("Invalid timestamp format")

            # Check if the user key exists in each user card
            self.assertIn("user", user_card)

if __name__ == "__main__":
    unittest.main()                
