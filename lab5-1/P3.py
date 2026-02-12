'''
Khanon Chroenphanupong
663040475-1
P3
'''

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QFrame, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class BMICalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adult and Child BMI Calculator")
        self.setFixedWidth(400) 
        self.setStyleSheet("background-color: #f0f0f0;") 
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        header = QLabel("Adult and Child BMI Calculator")
        header.setStyleSheet("""
            background-color: #c0504d; 
            color: white; 
            font-weight: bold; 
            padding: 5px;
            border: 1px solid #a0403d;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Arial", 11))
        main_layout.addWidget(header)

        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(10, 5, 10, 5)
        grid_layout.setSpacing("😎")

        label_for = QLabel("Calculate BMI for")
        grid_layout.addWidget(label_for, 0, 0, Qt.AlignmentFlag.AlignRight)
        age_combo = QComboBox()
        age_combo.addItems(["Adult Age 20+", "Child Age 2-19"])
        age_combo.setFixedWidth(150)
        grid_layout.addWidget(age_combo, 0, 1, 1, 2)

        grid_layout.addWidget(QLabel("Weight:"), 1, 0, Qt.AlignmentFlag.AlignRight)
        weight_input = QLineEdit()
        weight_input.setFixedWidth(70)
        grid_layout.addWidget(weight_input, 1, 1)
        
        weight_unit = QComboBox()
        weight_unit.addItems(["pounds", "kilograms", "stones (+lb)"]) #
        weight_unit.setFixedWidth(110)
        grid_layout.addWidget(weight_unit, 1, 2)

        grid_layout.addWidget(QLabel("Height:"), 2, 0, Qt.AlignmentFlag.AlignRight)
        height_input = QLineEdit()
        height_input.setFixedWidth(70)
        grid_layout.addWidget(height_input, 2, 1)
        
        height_unit = QComboBox()
        height_unit.addItems(["feet", "inches", "centimeters", "meters"]) #
        height_unit.setFixedWidth(110)
        grid_layout.addWidget(height_unit, 2, 2)

        inches_input = QLineEdit()
        inches_input.setFixedWidth(70)
        grid_layout.addWidget(inches_input, 3, 1)
        grid_layout.addWidget(QLabel("inches"), 3, 2)

        main_layout.addLayout(grid_layout)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(10, 0, 10, 0)
        clear_btn = QPushButton("Clear")
        clear_btn.setFixedWidth(75)
        calc_btn = QPushButton("Calculate")
        calc_btn.setFixedWidth(90)
        
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(calc_btn)
        main_layout.addLayout(btn_layout)

        answer_frame = QFrame()
        answer_frame.setFrameShape(QFrame.Shape.Box)
        answer_frame.setStyleSheet("background-color: white; border: 1px solid #c0c0c0; border-radius: 2px;")
        
        answer_vbox = QVBoxLayout(answer_frame)
        answer_vbox.setContentsMargins(10, 10, 10, 10)
        
        label_ans = QLabel("Answer:")
        label_ans.setStyleSheet("border: none;")
        answer_vbox.addWidget(label_ans)
        
        bmi_res = QLabel("BMI =")
        bmi_res.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bmi_res.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        bmi_res.setStyleSheet("border: none;")
        answer_vbox.addWidget(bmi_res)
        
        adult_label = QLabel("Adult BMI")
        adult_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        adult_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        adult_label.setStyleSheet("border: none;")
        answer_vbox.addWidget(adult_label)

        table = QTableWidget(4, 2)
        table.setHorizontalHeaderLabels(["BMI", "Status"])
        table.verticalHeader().setVisible(False) 
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setFixedHeight(150)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) 
        table.setStyleSheet("border: 1px solid #d0d0d0; gridline-color: #d0d0d0;")

        table_data = [
            ("< 18.5", "Underweight", "#fde395"), 
            ("18.5 - 24.9", "Healthy Weight", "#87d37c"), 
            ("25.0 - 29.9", "Overweight", "#f9b233"), 
            ("≥ 30.0", "Obese", "#ff6b6b") 
        ]

        for row, (bmi, status, color) in enumerate(table_data):
            bmi_item = QTableWidgetItem(bmi)
            bmi_item.setBackground(QColor(color))
            bmi_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 0, bmi_item)
            
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            table.setItem(row, 1, status_item)

        answer_vbox.addWidget(table)
        main_layout.addWidget(answer_frame)

        self.setLayout(main_layout)

if __name__ == '_main_':
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    window = BMICalculator()
    window.show()
    sys.exit(app.exec())