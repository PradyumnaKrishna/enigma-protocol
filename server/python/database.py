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
        except Error as e:
            print(e)

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

    def get_publicKey(self, id):
        """
        Gets a publicKey of user by id
        :param id: str
        :return: publicKey
        """
        query = f"SELECT publicKey FROM {PLAYLIST_TABLE} WHERE ID = ?"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchall()

        publicKey = result[0][0] if result else None
        return publicKey

    def update_last_activity(self, id):
        """
        updates the last_activity of a user
        :param id: str
        :return: None
        """
        query = f"UPDATE {PLAYLIST_TABLE} SET last_activity = ? WHERE ID = ?"
        self.cursor.execute(query, (datetime.now(), id))
        self.conn.commit()

    def save_user(self, publicKey):
        """
        saves the given publicKey in the table
        :param publicKey: str
        :return: id
        """
        id = secrets.token_hex(5)

        query = f"INSERT INTO {PLAYLIST_TABLE} VALUES (?, ?, ?)"
        self.cursor.execute(query, (id, publicKey, datetime.now()))
        self.conn.commit()

        return id
