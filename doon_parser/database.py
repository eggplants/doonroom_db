import sqlite3
from sqlite3 import Error
from typing import List


class DoonDatabase(object):
    def __init__(self, db_filepath: str, data: List[dict], table: str) -> None:
        self.db_filepath = db_filepath
        self.table = table

    def create_connection(db_file, sql):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
