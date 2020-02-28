import sqlite3
from db_connect import create_connection
from account import Account
from datetime import date

connection = create_connection()
cursor = connection.cursor()



def update_account_status(account_number):
    try:
        query = ''' UPDATE customer_details SET status=inactive WHERE accountNumber=?'''
        execute_query = cursor.execute(query, (account_number,)).fetchone()
    except Exception as exception:
     return exception

update_account_status("0705809845")