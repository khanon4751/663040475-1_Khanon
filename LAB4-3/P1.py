"""
Khanon Charoenphanupong
663040475-1
P1
"""

from LibraryItem import Book, TextBook, Magazine

print("--- Library System Test ---")

my_book = Book("Harry Potter", "B001", "J.K. Rowling")
my_book.set_pages(350)
my_book.check_out()
my_book.display_info()
    
my_textbook = TextBook("Python Programming", "T101", "Aj.namtarn", "Computer Science", 12)
my_textbook.display_info()
my_textbook.set_pages(350)
my_textbook.check_out()


my_mag = Magazine(202, "Geographic", "M555")
my_mag.display_info()
my_mag.check_out()
    
print("\n--- Returning Item ---")

my_book.return_item()
my_book.display_info()