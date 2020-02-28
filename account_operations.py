class AccountOperations:
    def __init__(self, account_number, status):
        self.account_number = account_number
        self.status = status
      
    

    def get_account_number(self):
        return self.account_number

    def get_status(self):
        return self.status


    def freeze_account(self, account):
        if (len(self.account_number) == 10 and self.account_number == account["account_number"]):
            account["status"] = "inactive"
        else:
            return "Invalid Operation"

