from Class import BankAccount

acc1 = BankAccount("John", "saving", 500)
acc2 = BankAccount("Tim", "loan", -1000000)
acc3 = BankAccount("Sarah", "saving", 0)

acc1.deposit(3000)
print(f"John Balance: {acc1.balance}")
print(f"Tim Balance: {acc2.balance}")
acc2.pay_loan(acc2.balance*-1/2)
acc3.deposit(50000000)

acc4 = BankAccount("Sarah", "loan", -100000000)
print(f"")
print(f"-----All Account Info-----")
print(f"")
acc1.print_customer()
acc2.print_customer()
acc3.print_customer()
acc4.print_customer()


