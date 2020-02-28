import sqlite3

def create_connection():
  try:
    connection = sqlite3.connect('account.db')
    return connection
  except Exception as exception:
    print("Error: ", exception)
