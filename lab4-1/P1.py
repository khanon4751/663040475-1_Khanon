"""
Khanon Charoenphanupong
663040475-1
Lab4-1 P1
"""
from cat import Cat
from datetime import datetime, timedelta

# Add 3 cats
cat1 = Cat("Navy", "Maine Coon", 1, "Ai")
cat2 = Cat("Ivory", "Persian", 2, "Bell")
cat3 = Cat("Ruby", "Birman", 2, "Chacha")

# For the first cat
print(f"1st Cate Date In: {cat1.get_time_in()}") # show date_in
cat1.greet() # Let the cat greets you

# For the second cat
print(f"2nd Cate Date Out: {cat2.get_time_out()}") # show date_out
# Change the date_out to be +2 days from now
new_date_out = datetime.now() + timedelta(days=2)
cat2.set_time_out(new_date_out)
# Show the date_out again
print(f"2nd Cate Date Out: {cat2.get_time_out()}") # show date_out (+2)

# For the third cat
cat3.owner = "Namfah" # Change name
cat3.age = 3 # Change age

# Show the details of all 3 cats
cat1.print_cat()
print()
cat2.print_cat()
print()
cat3.print_cat()

# Show the total number of cats in the class Cat so far
print(f"Total number of cats in the class Cat so far : {Cat.get_num()}")

# Reset the number of cats in the class Cat
Cat.reset_cat()
print("Cat number in the class Cat has been reset.")

# Show the total number of cats in the class Cat again (should be 0)
print(f"Total number of cats in the class Cat after reset: {Cat.get_num()}")