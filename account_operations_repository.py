import sqlite3
from db_connect import create_connection
from account import Account
from datetime import date

connection = create_connection()
cursor = connection.cursor()



def update_account_status(account_number, status):
    try:
        query = ''' UPDATE customer_details SET status=? WHERE accountNumber=?'''
        execute_query = cursor.execute(query, (status, account_number, )).fetchone()
        connection.commit()
        return execute_query
    except Exception as exception:
     return exception

# print(update_account_status("0705809845", "inactive"))