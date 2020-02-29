import sqlite3
from db_connect import create_connection
# from account_balance_repository import add_balance_detail
from account import Account
from datetime import date

connection = create_connection()
cursor = connection.cursor()

def get_row_count():
    try:
        query = ''' SELECT * FROM customer_details'''
        execute_query = cursor.execute(query).fetchall()
        row_count = len(execute_query)
        return row_count
    except Exception as exception:
        return exception

def add_customer(account_number, account_name, currency, 
    account_opening_date, last_transaction_date, account_type,
    bvn, full_name, status, phoneNumber=None, email=None):
    try:
        user_account = Account(account_number, account_name, currency, 
        account_opening_date, last_transaction_date, account_type,
        bvn, full_name, status, phoneNumber, email)
        print(user_account.status)
        customer_id = get_row_count()
        if (check_if_customer_exists(user_account.account_number)):
            return "Account Exists"
        elif(check_if_customer_exists(user_account.account_number) == False):
            query = '''INSERT INTO customer_details VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )'''
            execute_query = cursor.execute(query, (customer_id, user_account.account_number, user_account.account_name,
            user_account.currency, user_account.account_opening_date, user_account.last_transaction_date,
            user_account.account_type, user_account.bvn, user_account.full_name, 
            user_account.phone_number, user_account.email, user_account.status, get_todays_date(), ))
            connection.commit()
            # connection.close()
            return "Account Created"
        else:
            return "Error"
    except Exception as exception:
        return exception


def check_if_customer_exists(account_number):
    try:
        query = ''' SELECT id FROM customer_details WHERE accountNumber=?'''
        execute_query = cursor.execute(query, (account_number,)).fetchone()
        if execute_query == None:
            return False
        else:
            return True
    except Exception as exception:
        return exception

def get_customer_id(account_number):
    try:
        if check_if_customer_exists(account_number):
            query = ''' SELECT id FROM customer WHERE accountNumber=?'''
            execute_query = cursor.execute(query, (account_number, )).fetchone()
            customer_id = execute_query[0]
            return customer_id
        elif check_if_customer_exists(account_number) == False:
            return -1
    except Exception as exception:
        return exception

def get_account_number(customer_id):
    try:
        query = ''' SELECT accountNumber FROM customer_details WHERE id=?'''
        execute_query = cursor.execute(query, (customer_id, )).fetchone()
        return execute_query
    except Exception as exception:
        return exception
    
def get_account_details(account_number):
    if (check_if_customer_exists(account_number) == True):
        try:
            query = ''' SELECT id, accountName, currency, accountOpeningDate, lastTransactionDate,
            accountType, bvn, fullName, status, phoneNumber, email FROM customer_details WHERE accountNumber=?'''
            execute_query = cursor.execute(query, (account_number, )).fetchone()
            account_details = {
                "id": execute_query[0],
                "account_name": execute_query[1],
                "currency": execute_query[2],
                "account_opening_date": execute_query[3],
                "last_transaction_date": execute_query[4],
                "account_type": execute_query[5],
                "bvn": execute_query[6],
                "full_name": execute_query[7],
                "status": execute_query[8],
                "phone_number": execute_query[9],
                "email": execute_query[10],
                "account_number": account_number
            }
            return account_details
        except Exception as exception:
            return exception
    
def get_todays_date():
    today = str(date.today()).split("-")
    date_string = ""
    for day in range(len(today)):
        date_string = today[day] + "-" + date_string if (day != 0) else today[day] + date_string
    return date_string

def create_dummy_account():
    print(add_customer("0705809845", "Test", "NGN", get_todays_date(), get_todays_date(), "Savings",
    "459459805927438578578559", "Test TestUser", "active", "09052869373", "mail@mail.com"))

# print(get_account_details("0705809845"))
