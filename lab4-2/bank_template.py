"""
Khanon Charoenphanupong
663040475-1
Lab 4-2 : Bank Account - Revisited
bank_template
"""

class BankAccount:
    # Class attribute
    branch_name = "KKU Complex"
    branch_number = 1724
    last_loan_number = 0
    last_saving_number = 0

    # Private class attributes
    # account types
    __type_saving = 1
    __type_loan = 2

    # Constructor
    def __init__(self):
        pass
    
    # Instance methods
    def print_customer(self):
        pass
    
    def deposit(self, amount=0):
        self.balance += amount
        return self.balance
    
    def pay_loan(self, amount=0):
        self.balance += amount
        return self.balance