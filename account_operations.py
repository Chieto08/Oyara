class AccountOperations:
    def __init__(self, account_number, status=None):
        self.account_number = account_number
        self.status = status
      
    

    def get_account_number(self):
        return self.account_number

    def get_status(self):
        return self.status


    def freeze_account(self, account):
        if (len(self.account_number) == 10 and self.account_number == account["account_number"]):
            if (account["status"] == "active"):
                account["status"] = "inactive"
                return "Success"
            else:
                return "You can not freeze an inactive account"
        else:
            return "Invalid Operation"

    def unfreeze_account(self, account):
        if (len(self.account_number) == 10 and self.account_number == account["account_number"]):
            if (account["status"] == "inactive"):
                account["status"] = "active"
                return "Success"
            else:
                return "You can not unfreeze an active account"
        else:
            return "Invalid Operation"

