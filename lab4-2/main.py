"""
Khanon Charoenphanupong
663040475-1
Lab 4-2 : cat
Main Program
"""

from cat import Cat

cat1 = Cat("Milo", 3, "British Shorthair", "Gray")
cat2 = Cat.from_birth_year("Luna", 2015, "Siamese", "Cream")

print(cat1.meow())
print(cat1.play(2))
print(cat1.eat(50))
print(cat1.sleep(3))

print("\nCat1 Status:")
print(cat1.get_status())

print("\nIs Luna a senior cat?")
print(Cat.is_senior(cat2.age))

print("\nRecommended food for 4kg cat:")
print(Cat.calculate_healthy_food_amount(4), "grams")

print("\nSpecies Info:")
print(Cat.get_species_info())
