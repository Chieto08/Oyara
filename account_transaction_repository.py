import sqlite3
from db_connect import create_connection
from account_transactions import AccountTransactions
from account_repository import check_if_customer_exists
from datetime import date, datetime
import random

connection = create_connection()
cursor = connection.cursor()

def get_row_count():
    try:
        query = ''' SELECT * FROM transaction_details'''
        execute_query = cursor.execute(query).fetchall()
        row_count = len(execute_query)
        return row_count
    except Exception as exception:
        return exception

def generate_reference_id():
    reference_id = ""
    for i in range(20):
        reference_id += str(random.randint(0, 9999999999))
    return reference_id


def add_transaction_detail(account_number, amount, currency, debit_or_credit,
    narration, referenceId, transaction_time, type_of_transaction, value_date, balanceAfter=None, channel=None):
    try:
        transaction = AccountTransactions(account_number, amount, currency, 
        debit_or_credit, narration, referenceId,
        transaction_time, type_of_transaction, value_date, balanceAfter, channel)
        if (check_if_customer_exists(transaction.account_number) == True):
            transaction_id = get_row_count()
            if (check_if_transaction_exists(transaction.referenceId)):
                return "Transaction Exists"
            elif(check_if_transaction_exists(transaction.referenceId) == False):
                query = '''INSERT INTO transaction_details VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )'''
                execute_query = cursor.execute(query, (transaction_id, transaction.account_number, transaction.amount,
                transaction.currency, transaction.debit_or_credit, transaction.narration,
                transaction.referenceId, transaction.transaction_time, transaction.type_of_transaction, 
                transaction.balance_after, transaction.channel, transaction.value_date, get_todays_date(), ))
                connection.commit()
                connection.close()
                return "Transaction Created"
            else:
                return "Error"
        else:
            return "Invalid Operation!"
    except Exception as exception:
        return exception


def check_if_transaction_exists(referenceId):
    try:
        query = ''' SELECT id FROM transaction_details WHERE referenceId=?'''
        execute_query = cursor.execute(query, (referenceId,)).fetchone()
        if execute_query == None:
            return False
        else:
            return True
    except Exception as exception:
        print(exception)
        return exception

def get_transaction_id(referenceId):
    try:
        if check_if_transaction_exists(referenceId):
            query = ''' SELECT id FROM transaction_details WHERE referenceId=?'''
            execute_query = cursor.execute(query, (referenceId, )).fetchone()
            transaction_id = execute_query[0]
            return transaction_id
        elif check_if_transaction_exists(referenceId) == False:
            return -1
    except Exception as exception:
        return exception

def get_account_number(referenceId):
    try:
        query = ''' SELECT accountNumber FROM transaction_details WHERE referenceId=?'''
        execute_query = cursor.execute(query, (referenceId, )).fetchone()
        return execute_query
    except Exception as exception:
        return exception
    
def get_current_datetime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

def get_todays_date():
    today = str(date.today()).split("-")
    date_string = ""
    for day in range(len(today)):
        date_string = today[day] + "-" + date_string if (day != 0) else today[day] + date_string
    return date_string


# print(add_transaction_detail("0705809845", 500, "NGN", 
#     "Cr", "Opening transaction", generate_reference_id(), get_todays_date(),
#     "Credit", get_todays_date(), 1000, "POS")
# )