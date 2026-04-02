"""
Khanon Charoenphanupong
663040475-1
P1
"""

import sys
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox
)

from PySide6.QtCore import Qt, QLocale
from PySide6.QtGui import QColor


class StudentGradeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))

        self.setWindowTitle("P1: Student Scores and Grades")
        self.resize(950, 600)

        self.students = {}
        self.load_students()

        self.init_ui()
        self.apply_styles()

    # Load student file
    def load_students(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, "students.txt")

        if not os.path.exists(file_path):
            print("students.txt not found")
            return

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    student_id, name = line.split(",")
                    self.students[student_id.strip()] = name.strip()
                except ValueError:
                    print("Invalid format:", line)

    # UI
    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        grid = QGridLayout()

        # Student ID
        self.id_combo = QComboBox()
        self.id_combo.addItem("Select Student ID")
        self.id_combo.addItems(self.students.keys())
        self.id_combo.currentIndexChanged.connect(self.show_name)

        # Student Name
        self.name_label = QLabel("")
        self.name_label.setObjectName("nameLabel")
        self.name_label.setFixedHeight(30)

        # Score Inputs
        self.math_input = QSpinBox()
        self.math_input.setRange(0, 100)
        self.math_input.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.math_input.setAlignment(Qt.AlignCenter)
        self.math_input.setButtonSymbols(QSpinBox.UpDownArrows)
        self.math_input.setReadOnly(False)

        self.science_input = QSpinBox()
        self.science_input.setRange(0, 100)
        self.science_input.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.science_input.setAlignment(Qt.AlignCenter)
        self.science_input.setButtonSymbols(QSpinBox.UpDownArrows)
        self.science_input.setReadOnly(False)


        self.english_input = QSpinBox()
        self.english_input.setRange(0, 100)
        self.english_input.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.english_input.setAlignment(Qt.AlignCenter)
        self.english_input.setButtonSymbols(QSpinBox.UpDownArrows)
        self.english_input.setReadOnly(False)
        self.math_input.setFocusPolicy(Qt.StrongFocus)
        self.science_input.setFocusPolicy(Qt.StrongFocus)
        self.english_input.setFocusPolicy(Qt.StrongFocus)



        # Layout
        grid.addWidget(QLabel("Student ID:"), 0, 0)
        grid.addWidget(self.id_combo, 0, 1)

        grid.addWidget(QLabel("Student Name:"), 0, 2)
        grid.addWidget(self.name_label, 0, 3)

        grid.addWidget(QLabel("Math:"), 1, 0)
        grid.addWidget(self.math_input, 1, 1)

        grid.addWidget(QLabel("Science:"), 1, 2)
        grid.addWidget(self.science_input, 1, 3)

        grid.addWidget(QLabel("English:"), 1, 4)
        grid.addWidget(self.english_input, 1, 5)

        # Buttons
        button_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add Student")
        self.reset_btn = QPushButton("Reset Input")
        self.clear_btn = QPushButton("Clear All")

        self.add_btn.clicked.connect(self.add_student)
        self.reset_btn.clicked.connect(self.reset_input)
        self.clear_btn.clicked.connect(self.clear_all)

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.clear_btn)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels([
            "Student ID", "Name", "Math",
            "Science", "English",
            "Total", "Average", "Grade"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)

        # Add layouts
        main_layout.addLayout(grid)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # Show Name
    def show_name(self):
        student_id = self.id_combo.currentText()

        if student_id == "Select Student ID":
            self.name_label.setText("")
        else:
            self.name_label.setText(self.students.get(student_id, ""))

    # Add Student
    def add_student(self):
        student_id = self.id_combo.currentText()

        if student_id == "Select Student ID":
            QMessageBox.warning(self, "Warning", "Please select a student ID")
            return

        name = self.students.get(student_id, "")

        math = self.math_input.value()
        science = self.science_input.value()
        english = self.english_input.value()

        total = math + science + english
        average = total / 3
        grade = self.calculate_grade(average)

        self.table.setSortingEnabled(False)

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        data = [
            student_id, name, math,
            science, english,
            total, f"{average:.2f}", grade
        ]

        for col, value in enumerate(data):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignCenter)

            if col in [2, 3, 4] and int(data[col]) < 40:
                item.setBackground(QColor("red"))

            if col == 7 and grade == "F":
                item.setBackground(QColor("red"))

            self.table.setItem(row_position, col, item)

        self.table.setSortingEnabled(True)
        self.table.sortItems(0, Qt.AscendingOrder)


    def calculate_grade(self, avg):
        if avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"

    def sort_table(self):
        self.table.sortItems(0)

    def reset_input(self):
        self.id_combo.setCurrentIndex(0)
        self.math_input.setValue(0)
        self.science_input.setValue(0)
        self.english_input.setValue(0)

    def clear_all(self):
        self.table.setRowCount(0)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
                background-color: #f5f5f5;
            }

            QComboBox, QSpinBox {
                padding: 5px;
                border: 1px solid #aaa;
                border-radius: 5px;
                background-color: white;
            }
            
            QSpinBox:focus {
            border: 2px solid #3d85c6;
            background-color: #ffffff;
            }
            
            QLabel {
                font-weight: bold;
            }

            #nameLabel {
                background-color: #f4f1de;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }

            QPushButton {
                background-color: #6fa8dc;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #3d85c6;
            }

            QTableWidget {
                background-color: white;
                gridline-color: #ccc;
            }

            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 6px;
                font-weight: bold;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentGradeApp()
    window.show()
    sys.exit(app.exec())