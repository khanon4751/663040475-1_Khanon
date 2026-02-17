"""
Khanon Charoenphanupong
663040475-1
P2
"""

import sys
import math
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QGridLayout, QPushButton, QLineEdit, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class SimpleCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(320, 500)
        self.setStyleSheet("background-color: #f3f3f3;") 
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.header_label = QLabel("Standard")
        self.header_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.header_label.setStyleSheet("margin-bottom: 10px; color: #333;")
        main_layout.addWidget(self.header_label)

        self.display = QLineEdit()
        self.display.setFixedHeight(70)
        self.display.setFont(QFont("Segoe UI", 28))
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)

        self.display.setStyleSheet("border: none; background: transparent; padding-right: 5px;")
        main_layout.addWidget(self.display)

        grid = QGridLayout()
        grid.setSpacing(2) 

        buttons = [
            ('%', 0, 0), ('CE', 0, 1), ('C', 0, 2), ('<-', 0, 3),
            ('1/x', 1, 0), ('x^2', 1, 1), ('sqrt(x)', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('x', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('+/-', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3)
        ]

        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(72, 50)
            btn.setFont(QFont("Segoe UI", 11))
            
            if text.isdigit() or text == '.':
                btn.setStyleSheet("QPushButton { background-color: #ffffff; border: 1px solid #e0e0e0; } "
                                 "QPushButton:hover { background-color: #f9f9f9; }")
            elif text == '=':
                btn.setStyleSheet("QPushButton { background-color: #0067c0; color: white; border: none; } "
                                 "QPushButton:hover { background-color: #005aab; }")
            else:
                btn.setStyleSheet("QPushButton { background-color: #fafafa; border: 1px solid #e0e0e0; } "
                                 "QPushButton:hover { background-color: #f0f0f0; }")

            btn.clicked.connect(self.on_click)
            grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def on_click(self):
        button = self.sender()
        text = button.text()
        current_val = self.display.text()

        try:
            if text == "C" or text == "CE":
                self.display.clear()
            
            elif text == "<-":
                self.display.setText(current_val[:-1])
            
            elif text == "=":
                expression = current_val.replace('x', '*')
                result = eval(expression)
                self.display.setText(str(result))

            elif text == "1/x":
                val = float(current_val)
                self.display.setText(str(1 / val))

            elif text == "x^2":
                val = float(current_val)
                self.display.setText(str(val ** 2))

            elif text == "sqrt(x)":
                val = float(current_val)
                self.display.setText(str(math.sqrt(val)))

            elif text == "+/-":
                if not current_val: return
                if current_val.startswith('-'):
                    self.display.setText(current_val[1:])
                else:
                    self.display.setText("-" + current_val)

            else:
                self.display.setText(current_val + text)
                
        except Exception:
            self.display.setText("Error")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = SimpleCalculator()
    calc.show()
    sys.exit(app.exec())