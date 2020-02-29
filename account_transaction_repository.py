import sqlite3
from db_connect import create_connection
from account_transactions import AccountTransactions
from account_repository import check_if_customer_exists
from datetime import date, datetime
import random

def get_row_count():
    connection = create_connection()
    cursor = connection.cursor()
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
        reference_id += str(random.randint(0, 99))
    return reference_id


def add_transaction_detail(account_number, amount, currency, debit_or_credit,
    narration, referenceId, transaction_time, type_of_transaction, value_date, balanceAfter=None, channel=None):
    connection = create_connection()
    cursor = connection.cursor()
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
                transaction.currency, transaction.channel, transaction.debit_or_credit, transaction.narration,
                transaction.referenceId, transaction.transaction_time, transaction.type_of_transaction, 
                transaction.value_date, transaction.balance_after, get_todays_date(), ))
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
    connection = create_connection()
    cursor = connection.cursor()
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
    connection = create_connection()
    cursor = connection.cursor()
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

def get_transactions_by_account_no(account_number):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        if check_if_customer_exists(account_number):
            query = ''' SELECT * FROM transaction_details WHERE accountNumber=?'''
            execute_query = cursor.execute(query, (account_number, )).fetchall()
            all_transactions = []
            print(execute_query)
            for det in execute_query:
                transaction = {
                    "id": det[0],
                    "account_number": det[1],
                    "amount": det[2],
                    "currency": det[3],
                    "channel": det[4],
                    "debit_or_credit": det[5],
                    "narration": det[6],
                    "reference_id": det[7],
                    "transaction_time": det[8],
                    "transaction_type": det[9],
                    "value_date": det[10], 
                    "balance_after": det[11]
                }
                all_transactions.append(transaction)
            return all_transactions
        elif check_if_customer_exists(account_number) == False:
            return -1
    except Exception as exception:
        return exception


def get_debit_charge(amount, channel, account_number):
    if (channel == "e-channel"):
        if amount < 5000:
            charge_fee = (5/100) * amount
            if (charge_fee < 10):
                return charge_fee
            else:
                return 10
        elif amount > 5000 and amount < 50000:
            charge_fee = (4.5/100) * amount
            if (charge_fee < 25):
                return charge_fee
            else:
                return 25
        elif amount > 50000:
            charge_fee = (3/100) * amount
            if (charge_fee < 50):
                return charge_fee
            else:
                return 50
    elif channel == "POS":
        charge_fee = (0.75/100) * amount
        if charge_fee < 1200:
            return charge_fee
        else:
            return 1200
    elif channel == "ATM":
        all_transactions = get_transactions_by_account_no(account_number)
        monthly_transactions = []

        for transaction in all_transactions:
            if (transaction["transaction_time"].split("-")[1] == get_current_datetime().split("-")[1] and transaction["channel"] == "ATM"):
                monthly_transactions.append(transaction)

        if len(monthly_transactions) + 1 > 3:
            return 35
        else:
            return 0




def get_transactions_by_channel(account_number, channel):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        if check_if_customer_exists(account_number):
            query = ''' SELECT * FROM transaction_details WHERE accountNumber=? AND channel=?'''
            execute_query = cursor.execute(query, (account_number, channel, )).fetchall()
            all_transactions = []
            for det in execute_query:
                transaction = {
                    "id": det[0],
                    "account_number": det[1],
                    "amount": det[2],
                    "currency": det[3],
                    "channel": det[4],
                    "debit_or_credit": det[5],
                    "narration": det[6],
                    "reference_id": det[7],
                    "transaction_time": det[8],
                    "transaction_type": det[9],
                    "value_date": det[10], 
                    "balance_after": det[11]
                }
                all_transactions.append(transaction)
            return all_transactions
        elif check_if_customer_exists(account_number) == False:
            return -1
    except Exception as exception:
        return exception

def get_transactions_by_reference(account_number, reference_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        if check_if_customer_exists(account_number):
            query = ''' SELECT * FROM transaction_details WHERE accountNumber=? AND referenceId=?'''
            execute_query = cursor.execute(query, (account_number, reference_id, )).fetchall()
            all_transactions = []
            for det in execute_query:
                transaction = {
                    "id": det[0],
                    "account_number": det[1],
                    "amount": det[2],
                    "currency": det[3],
                    "channel": det[4],
                    "debit_or_credit": det[5],
                    "narration": det[6],
                    "reference_id": det[7],
                    "transaction_time": det[8],
                    "transaction_type": det[9],
                    "value_date": det[10], 
                    "balance_after": det[11]
                }
                all_transactions.append(transaction)
            return all_transactions
        elif check_if_customer_exists(account_number) == False:
            return -1
    except Exception as exception:
        return exception

def get_account_number(referenceId):
    connection = create_connection()
    cursor = connection.cursor()
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


# print(get_transactions_per_month("0705809845"))
# print(add_transaction_detail("0705809845", 500, "NGN", 
#     "Cr", "Opening transaction", generate_reference_id(), get_current_datetime(),
#     "Credit", get_todays_date(), 1000, "POS")
# )