"""
Khanon Charoenphanupong
663040475-1
Lab 4-2 : Bank Account - Revisited
P1
"""

from bank_template import BankAccount

# -------------------------------
# Create accounts
# -------------------------------
john = BankAccount("John", "saving", 500)
tim = BankAccount("Tim", "loan", -1_000_000)   # ❗ loan ต้องเป็นค่าติดลบ
sarah = BankAccount("Sarah", "saving", 0)

# -------------------------------
# Change branch name
# -------------------------------
BankAccount.change_branch_name("KMUTT Branch")

# -------------------------------
# John deposit and withdraw
# -------------------------------
john.deposit(3000)
john.withdraw(1000)

# -------------------------------
# Tim loan operations
# -------------------------------
tim.pay_loan(200000)     # จ่ายหนี้ → balance เข้าใกล้ 0
tim.get_loan(30000)      # กู้เพิ่ม (balance ≥ -50000 ถึงจะได้)

# -------------------------------
# Sarah deposit
# -------------------------------
sarah.deposit(50_000_000)

# -------------------------------
# Print account information
# -------------------------------
print("----- Account Information -----")
print(f"Branch: {BankAccount.branch_name}")
print(f"{john.name}: type={john.acc_type}, balance={john.balance:.2f}")
print(f"{tim.name}: type={tim.acc_type}, balance={tim.balance:.2f}")
print(f"{sarah.name}: type={sarah.acc_type}, balance={sarah.balance:.2f}")

# -------------------------------
# Loan interest plan
# -------------------------------
print()
BankAccount.calc_interest(1000, 5, 100)