class AccountBalance:
    def __init__(self, account_number, currency, available_balance, cleared_balance=None, unclear_balance=None, hold_balance=None, minimum_balance=None):
        self.account_number = account_number
        self.currency = currency
        self.available_balance = available_balance
        self.cleared_balance = cleared_balance
        self.unclear_balance = unclear_balance
        self.hold_balance = hold_balance
        self.minimum_balance = minimum_balance
    

    def get_account_number(self):
            return self.account_number

    def get_currency(self):
            return self.currency

    def get_available_balance(self):
            return self.available_balance

    def get_cleared_balance(self):
            return self.cleared_balance

    def get_unclear_balance(self):
            return self.unclear_balance

    def get_hold_balance(self):
            return self.hold_balance

    def get_minimum_balance(self):
            return self.minimum_balance
