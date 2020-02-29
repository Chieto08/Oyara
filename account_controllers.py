from bottle import get, post, request, run, route, template, redirect, static_file, error
from account_repository import create_dummy_account, get_account_details
from account_transactions import AccountTransactions
from account_balance_repository import get_account_balance_details, add_balance_detail, create_dummy_balance_for_account, update_account_balance
from account_transaction_repository import generate_reference_id, get_todays_date, get_current_datetime, add_transaction_detail, get_transactions_by_account_no, get_transactions_by_channel, get_transactions_by_reference, get_debit_charge
from account_operations import AccountOperations
from account_operations_repository import update_account_status
from account_table import create_tables
import json
import time
import os
from db_connect import create_connection


create_tables()
create_dummy_account()
create_dummy_balance_for_account()

@route('/account/debit/', method=['POST'])
def debit_account():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        account_number = request.forms.get('account_number')
        amount = request.forms.get('amount')
        currency = request.forms.get('currency')
        debit_or_credit = request.forms.get('debit_or_credit')
        narration = request.forms.get('narration')
        type_of_transaction = request.forms.get('type_of_transaction')
        channel = request.forms.get('channel')

        transaction = AccountTransactions(account_number, amount, currency,
        debit_or_credit, narration, generate_reference_id(), get_current_datetime(),
        type_of_transaction, get_todays_date(), channel)
        
        details_of_account = get_account_details(account_number)
        
        account_balance_details = get_account_balance_details(account_number)
        debit_charge = get_debit_charge(amount, channel, account_number)
        debit_response = transaction.debit_account(int(transaction.amount) + int(debit_charge), details_of_account, account_balance_details)
        
        if (debit_response is "Success"):
            update_account_balance(account_number, account_balance_details["available_balance"])

        account_balance_details = get_account_balance_details(account_number)
        
        add_transaction = add_transaction_detail(account_number, amount, currency,
        debit_or_credit, narration, generate_reference_id(), get_current_datetime(),
        type_of_transaction, get_todays_date(), account_balance_details["available_balance"], channel)
        

        add_balance = add_balance_detail(account_number, currency, account_balance_details["available_balance"],
        account_balance_details["cleared_balance"], account_balance_details["unclear_balance"], account_balance_details["hold_balance"],
        account_balance_details["minimum_balance"])

        if (debit_response is "Success"):
            data =	{
                    "message": "Debit operation successful!",
                    "status": "OK",
                    "Available Balance": account_balance_details["available_balance"],
                    "success":  True 
                    }
        else:
            data =	{
                    "message": debit_response,
                    "status": "Failed",
                    "Available Balance": account_balance_details["available_balance"],
                    "success":  False
                }
        response = json.dumps(data)
        return response
    except Exception as exception:
        return exception


@route('/account/credit/', method=['POST'])
def credit_account():
    try:
        account_number = request.forms.get('account_number')
        amount = request.forms.get('amount')
        currency = request.forms.get('currency')
        debit_or_credit = request.forms.get('debit_or_credit')
        narration = request.forms.get('narration')
        type_of_transaction = request.forms.get('type_of_transaction')
        channel = request.forms.get('channel')

        transaction = AccountTransactions(account_number, amount, currency,
        debit_or_credit, narration, generate_reference_id(), get_current_datetime(),
        type_of_transaction, get_todays_date(), channel)
        
        details_of_account = get_account_details(account_number)
        
        account_balance_details = get_account_balance_details(account_number)
        print(account_balance_details)
        credit_response = transaction.credit_account(transaction.amount, details_of_account, account_balance_details)
    

        if (credit_response == "Success"):
            update_account_balance(account_number, account_balance_details["available_balance"])

        
        account_balance_details = get_account_balance_details(account_number)
        
        add_transaction = add_transaction_detail(account_number, amount, currency,
        debit_or_credit, narration, generate_reference_id(), get_current_datetime(),
        type_of_transaction, get_todays_date(), account_balance_details["available_balance"], channel)
        print(add_transaction)
       
        add_balance = add_balance_detail(account_number, currency, account_balance_details["available_balance"],
        account_balance_details["cleared_balance"], account_balance_details["unclear_balance"], account_balance_details["hold_balance"],
        account_balance_details["minimum_balance"])

        if (credit_response == "Success"):
            data =	{
                    "message": "Credit operation successful!",
                    "status": "OK",
                    "Available Balance": account_balance_details["available_balance"],
                    "success":  True 
                    }
        else:
            data =	{
                    "message": credit_response,
                    "status": "Failed",
                    "Available Balance": account_balance_details["available_balance"],
                    "success":  False
                }
        response = json.dumps(data)
        return response
    except Exception as exception:
        return exception

@route('/account/freeze/', method=['POST'])
def freeze_account():
    try:
        account_number = request.forms.get('account_number')
        
        details_of_account = get_account_details(account_number)
        operation = AccountOperations(account_number)
        
        response = operation.freeze_account(details_of_account)
        
        if (response  == "Success"):
            update_account_status(account_number, details_of_account["status"])
        details_of_account = get_account_details(account_number)
        
        if (response  == "Success"):
            data =	{
                    "message": "Operation successful!",
                    "status": "OK",
                    "Account Status": details_of_account["status"],
                    "success":  True 
                    }
        else:
            data =	{
                    "message": response,
                    "status": "Failed",
                    "Account Status": details_of_account["status"],
                    "success":  False
                }
        response = json.dumps(data)
        return response
    except Exception as exception:
        return exception


@route('/account/unfreeze/', method=['POST'])
def unfreeze_account():
    try:
        account_number = request.forms.get('account_number')
        
        details_of_account = get_account_details(account_number)
        operation = AccountOperations(account_number)
        
        response = operation.unfreeze_account(details_of_account)
        

        if (response == "Success"):
            update_account_status(account_number, details_of_account["status"])
        details_of_account = get_account_details(account_number)
      
        if (response == "Success"):
            data =	{
                    "message": "Operation successful!",
                    "status": "OK",
                    "Account Status": details_of_account["status"],
                    "success":  True 
                    }
        else:
            data =	{
                    "message": response,
                    "status": "Failed",
                    "Account Status": details_of_account["status"],
                    "success":  False
                }
        response = json.dumps(data)
        return response
    except Exception as exception:
        return exception


@route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)

@route('/account/getAllTransactions/<account_number>')
def getCustomerTransactions(account_number=None):
    try:
        transactions = get_transactions_by_account_no(account_number)
        data =	{
                "message": "Operation successful!",
                "status": "OK",
                "Transactions": transactions,
                "success":  True 
                }
    
        response = json.dumps(data)
        return response
    except Exception as exception:
        return exception

@route('/account/getAllTransactions/<account_number>/<channel>')
def getCustomerTransactions(account_number=None, channel=None):
    try:
        transactions = get_transactions_by_channel(account_number, channel)
        data =	{
                    "message": "Operation successful!",
                    "status": "OK",
                    "Transactions": transactions,
                    "success":  True 
                    }
       
        response = json.dumps(data)
        return response
    except Exception as exception:
        return exception

@route('/account/getAllTransactions/<account_number>/<reference>')
def getCustomerTransactions(account_number=None, reference=None):
    try:
        transactions = get_transactions_by_reference(account_number, reference)
        data =	{
                    "message": "Operation successful!",
                    "status": "OK",
                    "Transactions": transactions,
                    "success":  True 
                    }
       
        response = json.dumps(data)
        return response
    except Exception as exception:
        return exception


run(host='localhost', port=8080, debug=True)

