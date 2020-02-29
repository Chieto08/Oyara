import sqlite3
from db_connect import create_connection
from account_balance import AccountBalance
from account_repository import check_if_customer_exists
from datetime import date
import random

connection = create_connection()
cursor = connection.cursor()

def get_row_count():
    try:
        query = ''' SELECT * FROM customer_balance'''
        execute_query = cursor.execute(query).fetchall()
        row_count = len(execute_query)
        return row_count
    except Exception as exception:
        return exception


def add_balance_detail(account_number, currency, available_balance, cleared_balance=None,
              unclear_balance=None, hold_balance=None, minimum_balance=None):
    try:
        balance = AccountBalance(account_number, currency, 
        available_balance, cleared_balance, unclear_balance, hold_balance, minimum_balance)
        if (check_if_customer_exists(balance.account_number) == True):
            balance_id = get_row_count()
            query = '''INSERT INTO customer_balance VALUES(?, ?, ?, ?, ?, ?, ?, ?, ? )'''
            execute_query = cursor.execute(query, (balance_id, balance.account_number,
            balance.currency, balance.available_balance, balance.cleared_balance,
            balance.unclear_balance, balance.hold_balance, balance.minimum_balance, get_todays_date(), ))
            connection.commit()
            # connection.close()
            return "Balance log Created"
        else:
            return "Invalid Operation!"
    except Exception as exception:
        return exception

def get_account_balance_details(account_number):
    if (check_if_customer_exists(account_number) == True):
        try:
            connection = create_connection()
            query = ''' SELECT id, currency, availableBalance, clearedBalance,
            unclearBalance, holdBalance, minimumBalance FROM customer_balance WHERE accountNumber=?'''
            execute_query = cursor.execute(query, (account_number, )).fetchone()
            account_balance_details = {
                "id": execute_query[0],
                "currency": execute_query[1],
                "available_balance": execute_query[2],
                "cleared_balance": execute_query[3],
                "unclear_balance": execute_query[4],
                "hold_balance": execute_query[5],
                "minimum_balance": execute_query[6]
            }
            return account_balance_details
        except Exception as exception:
            return exception

def get_balance_id(account_number):
    try:
        connection = create_connection()
        if check_if_customer_exists(account_number):
            query = ''' SELECT id FROM customer_balance WHERE accountNumber=?'''
            execute_query = cursor.execute(query, (balance_id, )).fetchone()
            customer_balance_id = execute_query[0]
            return customer_balance_id
        elif check_if_customer_exists(balance_id) == False:
            return -1
    except Exception as exception:
        return exception

def update_account_balance(account_number, new_balance):
    try:
        connection = create_connection()
        query = ''' UPDATE customer_balance SET availableBalance=? WHERE accountNumber=?'''
        execute_query = cursor.execute(query, (new_balance, account_number,)).fetchone()
        connection.commit()
        connection.close()
    except Exception as exception:
        return exception

def get_account_number(balance_id):
    try:
        connection = create_connection()
        query = ''' SELECT accountNumber FROM customer_balance WHERE id=?'''
        execute_query = cursor.execute(query, (balance_id, )).fetchone()
        return execute_query
    except Exception as exception:
        return exception
    
    
def get_todays_date():
    today = str(date.today()).split("-")
    date_string = ""
    for day in range(len(today)):
        date_string = today[day] + "-" + date_string if (day != 0) else today[day] + date_string
    return date_string

def create_dummy_balance_for_account():
    print(add_balance_detail("0705809845", "NGN", 500, 0, 0, 0, 0))