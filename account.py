class Account:
    def __init__(self, account_number, account_name, currency, account_opening_date, last_transaction_date, account_type, bvn, full_name, status, phone_number=None, email=None):

        self.account_number = account_number
        self.account_name = account_name
        self.currency = currency
        self.account_opening_date = account_opening_date
        self.last_transaction_date = last_transaction_date
        self.account_type = account_type
        self.bvn = bvn
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.status = status

    def get_account_number(self):
        return self.account_number

    def get_account_name(self):
        return self.account_name

    def get_currency(self):
        return self.currency

    def get_account_opening_date(self):
        return self.account_opening_date

    def get_last_transaction_date(self):
        return self.last_transaction_date

    def get_account_type(self):
        return self.account_type

    def get_bvn(self):
        return self.bvn

    def get_full_name(self):
        return self.full_name

    def get_phone_number(self):
        return self.phone_number

    def get_email(self):
        return self.email

    def get_status(self):
        return self.status
