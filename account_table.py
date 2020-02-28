import sqlite3
from db_connect import create_connection

connection = create_connection()


def check_for_customer_details_table():
    try:
        query = (''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='customer_details' ''')
        execute_query = connection.execute(query).fetchone()
        if execute_query[0] == 1:
            return True
        else:
            return False
        connection.commit()
    except Exception as exception:
        print("Error customer_details_table: ", exception)

def check_for_customer_balance_table():
    try:
        query = (''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='customer_balance' ''')
        execute_query = connection.execute(query).fetchone()
        if execute_query[0] == 1:
            return True
        else:
            return False
        connection.commit()
    except Exception as exception:
        print("Error customer_balance_table: ", exception)

def check_for_transaction_details_table():
    try:
        query = (''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='transaction_details' ''')
        execute_query = connection.execute(query).fetchone()
        if execute_query[0] == 1:
            return True
        else:
            return False
        connection.commit()
    except Exception as exception:
        print("Error transaction_details_table: ", exception)

def create_tables():
    try:
        tables = ["customer_details", "customer_balance", "transaction_details"]
        for table in tables:
            if table == "customer_details" and check_for_customer_details_table():
                pass
            elif table == "customer_details" and (check_for_customer_details_table() == False):
                connection.execute("CREATE TABLE customer_details (id INTEGER, accountNumber char NOT NULL PRIMARY KEY, accountName char NOT NULL, \
                currency char NOT NULL, accountOpeningDate char NOT NULL, lastTransactionDate char NOT NULL, accountType char NOT NULL, \
                bvn INTEGER NOT NULL, fullname char NOT NULL, phoneNumber INTEGER, email char, status char NOT NULL, createdAt char)")
            elif table == "customer_balance" and check_for_customer_balance_table():
                pass
            elif table == "customer_balance" and (check_for_customer_balance_table() == False):
                connection.execute("CREATE TABLE customer_balance (id INTEGER PRIMARY KEY, accountNumber char NOT NULL, currency char NOT NULL, availableBalance INTEGER NOT NULL, \
                clearedBalance INTEGER, unclearBalance INTEGER, holdBalance INTEGER, minimumBalance INTEGER, createdAt char)")
            elif table == "transaction_details" and check_for_transaction_details_table():
                pass
            elif table == "transaction_details" and (check_for_transaction_details_table()  == False):
                connection.execute("CREATE TABLE transaction_details (id INTEGER, accountNumber char NOT NULL, amount INTEGER NOT NULL, currency char NOT NULL, \
                channel char, debitOrCredit char NOT NULL, narration char NOT NULL, referenceId char NOT NULL PRIMARY KEY, transactionTime char NOT NULL, \
                    transactionType char NOT NULL, valueDate char NOT NULL, balanceAfter INTEGER, createdAt char)")
        connection.commit()
        print("Tables created")
    except Exception as exception:
        print("Error: ", exception)


create_tables()