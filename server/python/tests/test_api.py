"""
Tests for Flask APIs
"""

import unittest

from main import app


class TestAPI(unittest.TestCase):
    """
    Test Flask APIs
    """

    def setUp(self):
        self.app = app.test_client()

    def test_home(self):
        """
        Test homepage
        """
        response = self.app.get("/")
        self.assertEqual(200, response.status_code)

    def test_new(self):
        """
        Test new user creation
        """
        public_key = "random-public-key"
        response = self.app.get(f"/login/{public_key}")
        self.assertEqual(200, response.status_code)

        user_id = response.json["user"]
        response = self.app.get(f"/connect/{user_id}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(public_key, response.json["publicKey"])

    def test_not_found(self):
        """
        Test user not found
        """
        user_id = "wrong-id"
        response = self.app.get(f"/connet/{user_id}")
        self.assertEqual(404, response.status_code)
