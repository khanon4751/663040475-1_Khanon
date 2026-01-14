"""
Khanon Charoenphanupong
663040475-1
P1
"""

from datetime import datetime

class LibraryItem:
    def __init__(self,title,item_id):
        self.title = title
        self._id = item_id
        self._check_out = False

    def get_status(self):
        return "Checked out" if self._check_out else "Available"
    
    def check_out(self):
        if not self._check_out:
            self._check_out = True
            return True
        return False
    
    def return_item(self):
        if self._check_out:
            self._check_out = False
            return True
        return False
    
    def display_info(self):
        print(f"Item: {self.title} | ID: {self._id} | Status: {self.get_status()}")

class Book(LibraryItem):
    def __init__(self,title,item_id,author):
        super().__init__(title, item_id)
        self.author = author
        self.pages_count = 0

    def set_pages(self,pages):
        self.pages_count = pages

    def display_info(self):
        print(f"Book: {self.title} | Author: {self.author} | Pages: {self.pages_count} | Status: {self.get_status()}")

class TextBook(Book):
    def __init__(self,title,item_id,author,subject,grade_level):
        super().__init__(title,item_id,author)
        self.subject = subject
        self.grade_level = grade_level

    def display_info(self):
        print(f"Textbook: {self.title} | Author: {self.author} | Pages: {self.pages_count} | Subject: {self.subject} | Grade: {self.grade_level}")

class Magazine(LibraryItem):
    def __init__(self,issue_number,title,item_id,):
        super().__init__(title,item_id)
        self.issue_number = issue_number
        self.month = datetime.now().month
        self.year = datetime.now().year

    def display_info(self):
        print(f"Magazine: {self.title} | ID: {self._id} | Issue: {self.issue_number} | Date: {self.month}/{self.year} | Status: {self.get_status()}")


    
              
    