"""
Tests database module
"""

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
