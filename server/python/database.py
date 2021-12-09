"""
DATABASE QUERY FOR READ AND WRITE
"""

import sqlite3
from sqlite3 import Error

from datetime import datetime
import secrets


FILE = "users.db"
PLAYLIST_TABLE = "Users"


class DataBase:
    """
    used to connect, write to and read from a local sqlite3 database
    """

    def __init__(self):
        """
        try to connect to file and create cursor
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(FILE)
        except Error as exception:
            print(exception)

        self.cursor = self.conn.cursor()
        self._create_table()

    def close(self):
        """
        close the db connection
        :return: None
        """
        self.conn.close()

    def _create_table(self):
        """
        create new database table if one doesn't exist
        :return: None
        """
        query = f"""CREATE TABLE IF NOT EXISTS {PLAYLIST_TABLE} (id TEXT PRIMARY KEY,
                    publicKey TEXT, last_activity DATE)"""
        self.cursor.execute(query)
        self.conn.commit()

    def get_public_key(self, identity):
        """
        Gets a publicKey of user by identity
        :param identity: str
        :return: publicKey
        """
        query = f"SELECT publicKey FROM {PLAYLIST_TABLE} WHERE ID = ?"
        self.cursor.execute(query, (identity,))
        result = self.cursor.fetchall()

        public_key = result[0][0] if result else None
        return public_key

    def update_last_activity(self, identity):
        """
        updates the last_activity of a user
        :param identity: str
        :return: None
        """
        query = f"UPDATE {PLAYLIST_TABLE} SET last_activity = ? WHERE ID = ?"
        self.cursor.execute(query, (datetime.now(), identity))
        self.conn.commit()

    def save_user(self, public_key):
        """
        saves the given public_key in the table
        :param public_key: str
        :return: identity
        """
        identity = secrets.token_hex(5)

        query = f"INSERT INTO {PLAYLIST_TABLE} VALUES (?, ?, ?)"
        self.cursor.execute(query, (identity, public_key, datetime.now()))
        self.conn.commit()

        return identity
