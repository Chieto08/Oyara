class AccountTransactions:
    def __init__(self, account_number, amount, currency, debit_or_credit, narration, referenceId, transaction_time, type_of_transaction, value_date, balance_after=None, channel=None, debit_param=None):
        self.account_number = account_number
        self.amount = amount
        self.currency = currency
        self.channel = channel
        self.debit_or_credit = debit_or_credit
        self.narration = narration
        self.referenceId = referenceId
        self.transaction_time = transaction_time
        self.type_of_transaction = type_of_transaction
        self.value_date = value_date
        self.balance_after = balance_after
        self.debit_param = debit_param
    

    def get_account_number(self):
        return self.account_number

    def get_amount(self):
        return self.amount

    def get_currency(self):
        return self.currency

    def get_channel(self):
        return self.channel

    def get_debit_or_credit(self):
        return self.debit_or_credit

    def get_narration(self):
        return self.narration

    def get_referenceId(self):
        return self.referenceId

    def get_transactionTime(self):
        return self.transaction_time

    def get_type_of_transaction(self):
        return self.type_of_transaction

    def get_valueDate(self):
        return self.valueDate

    def get_balanceAfter(self):
        return self.balance_after
        

    def debit_account(self, amount, account, account_balance):
        if (len(self.account_number) == 10 and self.account_number == account["account_number"]):
            if (account["status"] == "active"):
                if (self.currency == account["currency"]):
                    if (self.debit_or_credit == "Dr"):
                        if ((int(account_balance["available_balance"] - account_balance["minimum_balance"]) > int(amount)) or
                        (int(account_balance["available_balance"] - account_balance["minimum_balance"]) == int(amount))):
                            account_balance["available_balance"] = int(account_balance["available_balance"])
                            account_balance["available_balance"] -= int(amount)
                        else:
                            return "Insufficient Funds"
                    else:
                        return "Invalid Operation"
                else:
                    return "Invalid Currency"
            else:
                return "Invalid Operation"

    def credit_account(self, amount, account, account_balance):
        if (len(self.account_number) == 10 and self.account_number == account["account_number"]):
            if (account["status"] == "active"):
                if (self.currency == account["currency"]):
                    if (self.debit_or_credit == "Cr"):
                        account_balance["available_balance"] = int(account_balance["available_balance"])
                        account_balance["available_balance"] += int(amount)
                    else:
                        return "Invalid Operation"
                else:
                    return "Invalid Currency"
            else:
                return "Account not suitable for operation"
        else:
                return "Invalid Operation"

    def freeze_account(self, account):
        if (len(self.account_number) == 10 and self.account_number == account["account_number"]):
            account["status"] = "inactive"

