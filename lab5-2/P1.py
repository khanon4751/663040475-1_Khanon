"""
Khanon Charoenphanupong
663040475-1
P1
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                             QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QWidget, QLabel, QLineEdit)
from PySide6.QtWidgets import QPushButton, QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

kg = "kilograms"
lb = "pounds"
cm = "centimeters"
m = "meters"
ft = "feet"
adult = "Adults 20+"
child = "Children and Teenagers (5-19)"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("P1: BMI Calculator")
        self.setMinimumWidth(350)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        header = QLabel("Adult and Child BMI Calculator")
        header.setStyleSheet("background-color: #B22222; color: white; font-weight: bold; padding: 5px;")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 12))
        header.setFixedHeight(35)
        main_layout.addWidget(header)
        

        # Create an input section object
        self.input_section = InputSection()
        main_layout.addWidget(self.input_section)
        
        # create an output section object
        self.output_section = OutputSection()

        result_container = QWidget()
        result_container.setStyleSheet("background-color: #FAF0E6;")
        result_container.setLayout(self.output_section.layout)
        main_layout.addWidget(result_container)

        # connect signals from clicking submit and clear buttons
        self.input_section.btn_submit.clicked.connect(lambda: self.input_section.submit_reg(self.output_section))
        self.input_section.btn_clear.clicked.connect(lambda: self.input_section.clear_form(self.output_section))

class OutputSection(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.lbl_title = QLabel("Your BMI")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl_title)

        self.lbl_value = QLabel("0.00")
        self.lbl_value.setAlignment(Qt.AlignCenter)
        self.lbl_value.setStyleSheet("color: #6A5ACD; font-size: 24pt; font-weight: bold;")
        self.layout.addWidget(self.lbl_value)
        self.layout.addStretch()
        
    def show_adult_table(self):
        table_container = QWidget()
        table_layout = QGridLayout(table_container)
        
        label_bmi = QLabel("<b>BMI</b>")
        label_cond = QLabel("<b>Condition</b>")
        table_layout.addWidget(label_bmi, 0, 0, Qt.AlignCenter)
        table_layout.addWidget(label_cond, 0, 1, Qt.AlignCenter)
        
        data = [("< 18.5", "Thin"), ("18.5 - 25.0", "Normal"), 
                ("25.1 - 30.0", "Overweight"), ("> 30.0", "Obese")]
        
        for row, (b, c) in enumerate(data, 1):
            table_layout.addWidget(QLabel(b), row, 0, Qt.AlignCenter)
            table_layout.addWidget(QLabel(c), row, 1, Qt.AlignCenter)
            
        self.layout.addWidget(table_container)

    def show_child_link(self):
        info_text = QLabel("For child's BMI interpretation, please click one of the following links.")
        info_text.setWordWrap(True)
        info_text.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(info_text)

        link_layout = QHBoxLayout()
        boy_link = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-boys-z-5-19years.pdf?sfvrsn=4007e921_4">BMI graph for BOYS</a>')
        girl_link = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-girls-z-5-19years.pdf?sfvrsn=c708a56b_4">BMI graph for GIRLS</a>')
        boy_link.setOpenExternalLinks(True)
        girl_link.setOpenExternalLinks(True)
        link_layout.addWidget(boy_link)
        link_layout.addWidget(girl_link)
        self.layout.addLayout(link_layout)

    def update_results(self, bmi, age_group):
        self.clear_result()
        self.lbl_value.setText(f"{bmi:.2f}")
        if age_group == adult:
            self.show_adult_table()
        else:
            self.show_child_link()
    
    def clear_result(self):
        self.lbl_value.setText("0.00")
        while self.layout.count() > 2:
            item = self.layout.takeAt(2)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

class InputSection(QWidget):
    def __init__(self):
        super().__init__()
        form = QFormLayout(self)

        self.age_combo = QComboBox()
        self.age_combo.addItems([adult, child])
        form.addRow("BMI age group:", self.age_combo)

        self.weight_input = QLineEdit()
        self.weight_unit = QComboBox()
        self.weight_unit.addItems([kg, lb])
        w_layout = QHBoxLayout()
        w_layout.addWidget(self.weight_input)
        w_layout.addWidget(self.weight_unit)
        form.addRow("Weight:", w_layout)

        self.height_input = QLineEdit()
        self.height_unit = QComboBox()
        self.height_unit.addItems([cm, m, ft])
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.height_input)
        h_layout.addWidget(self.height_unit)
        form.addRow("Height:", h_layout)

        btn_box = QHBoxLayout()
        self.btn_clear = QPushButton("clear")
        self.btn_submit = QPushButton("Submit Registration")
        btn_box.addWidget(self.btn_clear)
        btn_box.addWidget(self.btn_submit)
        form.addRow(btn_box)

    def clear_form(self, output_section):
        self.weight_input.clear() 
        self.height_input.clear() 
        
        output_section.clear_result() 

    def submit_reg(self, output_section):
        bmi = self.calculate_BMI()
        if bmi:
            output_section.update_results(bmi, self.age_combo.currentText())

    def calculate_BMI(self):
        try:
            w = float(self.weight_input.text())
            h = float(self.height_input.text())
            
            if self.weight_unit.currentText() == lb:
                w = w * 0.453592
            
            h_unit = self.height_unit.currentText()
            if h_unit == cm: h = h / 100
            elif h_unit == ft: h = h * 0.3048
            
            return w / (h * h)
        except (ValueError, ZeroDivisionError):
            return None

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()