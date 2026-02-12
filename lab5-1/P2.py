'''
Natthida Sriphan
663040479-3
P2
'''

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QDateEdit, 
                             QRadioButton, QButtonGroup, QComboBox, QTextEdit, 
                             QCheckBox, QPushButton)
from PySide6.QtCore import QDate, Qt

class StudentRegistrationForm(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle("P2: Student Registration") 
        self.setFixedSize(400, 600) 

        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        
        title = QLabel("Student Registration Form") 
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title)
        main_layout.addSpacing(10)

        
        main_layout.addWidget(QLabel("Full Name:")) 
        self.name_input = QLineEdit()
        main_layout.addWidget(self.name_input)

        
        main_layout.addWidget(QLabel("Email:")) 
        self.email_input = QLineEdit()
        main_layout.addWidget(self.email_input)

        
        main_layout.addWidget(QLabel("Phone:")) 
        self.phone_input = QLineEdit()
        main_layout.addWidget(self.phone_input)

        
        main_layout.addWidget(QLabel("Date of Birth (dd/MM/yyyy):")) 
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True) 
        self.date_edit.setDisplayFormat("dd/MM/yyyy") 
        self.date_edit.setDate(QDate(2000, 1, 1)) 
        main_layout.addWidget(self.date_edit)
        self.date_edit.setFixedWidth(200)

        
        main_layout.addWidget(QLabel("Gender:")) 
        gender_layout = QHBoxLayout()
        self.gender_group = QButtonGroup(self) 
        
        genders = ["Male", "Female", "Non-binary", "Prefer not to say"] 
        for gender_text in genders:
            radio = QRadioButton(gender_text) 
            self.gender_group.addButton(radio)
            gender_layout.addWidget(radio)
        main_layout.addLayout(gender_layout)

        main_layout.addWidget(QLabel("Program:")) 
        self.program_combo = QComboBox()
        programs = [
            "Select your program", "Computer Engineering", "Digital Media Engineering",
            "Environmental Engineering", "Electical Engineering", "Semiconductor Engineering",
            "Mechanical Engineering", "Industrial Engineering", "Logistic Engineering",
            "Power Engineering", "Electronic Engineering", "Telecommunication Engineering",
            "Agricultural Engineering", "Civil Engineering", "ARIS"
        ]
        self.program_combo.addItems(programs)
        main_layout.addWidget(self.program_combo)

        
        main_layout.addWidget(QLabel("Tell us a little bit about yourself:")) 
        self.about_text = QTextEdit()
        self.about_text.setMaximumHeight(100) 
        main_layout.addWidget(self.about_text)

        self.terms_check = QCheckBox("I accept the terms and conditions.") 
        main_layout.addWidget(self.terms_check)

        main_layout.addSpacing(10) 
        self.submit_btn = QPushButton("Submit Registration") 
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.submit_btn)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

       
        central_widget.setLayout(main_layout)

if __name__ == '_main_':
    app = QApplication(sys.argv)
    window = StudentRegistrationForm()
    window.show()
    sys.exit(app.exec())