"""
Khanon Charoenphanupong
663040475-1
Lab4-1 P2
"""

from bank_template import BankAccount

# Create accounts
john = BankAccount()
john.name = "John"
john.acc_type = "saving"
john.balance = 500

tim = BankAccount()
tim.name = "Tim"
tim.acc_type = "loan"
tim.balance = -1_000_000

sarah = BankAccount()
sarah.name = "Sarah"
sarah.acc_type = "saving"
sarah.balance = 0

# John deposit 3,000
john.deposit(3000)
print(f"John balance: {john.balance:,}\n")

# Tim pays half of loan
loan_payment = abs(tim.balance) / 2
tim.pay_loan(loan_payment)

# Sarah deposit 50,000,000
sarah.deposit(50_000_000)

# Sarah opens loan account
sarah_loan = BankAccount()
sarah_loan.name = "Sarah"
sarah_loan.acc_type = "loan"
sarah_loan.balance = -100_000_000

# Show customer info (basic)
print(f"Name: {john.name}, Type: {john.acc_type}, Balance: {john.balance:,}")
print(f"Name: {tim.name}, Type: {tim.acc_type}, Balance: {tim.balance:,}")
print(f"Name: {sarah.name}, Type: {sarah.acc_type}, Balance: {sarah.balance:,}")
print(f"Name: {sarah_loan.name}, Type: {sarah_loan.acc_type}, Balance: {sarah_loan.balance:,}")