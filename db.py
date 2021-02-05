import sqlite3
import os
from sqlite3 import Error


class UserDB:
  def __init__(self, db_path: str):
    # Attempts to create a user table, if there is none
    self.conn = create_connection(db_path)


def create_connection(db_path: str):
  # Create database connection 
  conn = None

  try:
    conn = sqlite3.connect(os.path.abspath(db_path))
  except Error as e:
    print(e)
  finally:
    return conn

def close_connection(conn: sqlite3.Connection):
  conn.close()

def create_user_table():
  # Creates a user table, if there is none
