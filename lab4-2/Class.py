class BankAccount:
    branch_name = "KKU Complex"
    branch_number = 1724
    last_loan_number = 0
    last_saving_number = 0

    __type_saving = 1
    __type_loan = 2

    def __init__( self, name, type="saving", balance=0):
        self.name = name
        self.type = type
        self.balance = balance

        if self.type == "saving":
            BankAccount.last_saving_number += 1
            type_num = BankAccount.__type_saving
            run_num = BankAccount.last_saving_number
        else:
         BankAccount.last_loan_number += 1
         type_num = BankAccount.__type_loan
         run_num = BankAccount.last_loan_number
         
        self.account_number = f"{BankAccount.branch_number}-{type_num}-{run_num}"

    
    def print_customer(self):
        print(f"----- Customer Record -----")
        print(f"Name: {self.name}")
        print(f"Account number: {self.account_number}")
        print(f"Account type: {self.type}")
        print(f"Balance: {self.balance}")
        print(f"----- End Record -----")
        
    def deposit(self, amount=0):
        self.balance += amount
        return self.balance
    
    def pay_loan(self, amount=0):
        self.balance += amount
        return self.balance