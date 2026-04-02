"""
Khanon Charoenphanupong
663040475-1
P2
"""
import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QComboBox, QDoubleSpinBox, 
                             QPushButton, QLabel, QMessageBox, QFormLayout)
from PySide6.QtCharts import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis, QValueAxis, QStackedBarSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

class SalesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monthly Sales Tracker")
        self.resize(1000, 700)

        self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.categories = ["Electronics", "Clothing", "Food", "Others"]
        self.sales_data = {cat: [0.0] * 12 for cat in self.categories}

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        control_panel = QVBoxLayout()
        form_layout = QFormLayout()

        self.file_input = QLineEdit("sales_data.txt")
        self.month_input = QComboBox()
        self.month_input.addItems(self.months)
        
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 1000000)
        self.amount_input.setPrefix("฿")

        self.category_input = QComboBox()
        self.category_input.addItems(self.categories)

        form_layout.addRow("Filename:", self.file_input)
        form_layout.addRow("Month:", self.month_input)
        form_layout.addRow("Sales Amount:", self.amount_input)
        form_layout.addRow("Category:", self.category_input)

    
        self.btn_import = QPushButton("Import Data")
        self.btn_import.clicked.connect(self.import_data)
        
        self.btn_add = QPushButton("Add Data")
        self.btn_add.setStyleSheet("background-color: #e1f5fe;")
        self.btn_add.clicked.connect(self.add_manual_data)

        self.btn_clear = QPushButton("Clear Chart")
        self.btn_clear.clicked.connect(self.clear_data)

        control_panel.addLayout(form_layout)
        control_panel.addWidget(self.btn_import)
        control_panel.addWidget(self.btn_add)
        control_panel.addWidget(self.btn_clear)
        control_panel.addStretch()


        self.chart = QChart()
        self.chart.setTitle("Monthly Sales by Category")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        main_layout.addLayout(control_panel, 1)
        main_layout.addWidget(self.chart_view, 3)

        self.update_chart()

    def update_chart(self):
        self.chart.removeAllSeries()
        
        series = QStackedBarSeries()

        for category in self.categories:
            bar_set = QBarSet(category)
            bar_set.append(self.sales_data[category])
            series.append(bar_set)

        self.chart.addSeries(series)

        self.chart.removeAxis(self.chart.axisX())
        self.chart.removeAxis(self.chart.axisY())

        axis_x = QBarCategoryAxis()
        axis_x.append(self.months)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText("Amount (฿)")
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

    def add_manual_data(self):
        month_idx = self.month_input.currentIndex()
        category = self.category_input.currentText()
        amount = self.amount_input.value()

        self.sales_data[category][month_idx] += amount
        self.update_chart()

    def import_data(self):
        filename = self.file_input.text()
        if not os.path.exists(filename):
            QMessageBox.warning(self, "File Not Found", f"Could not find {filename}")
            return

        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        m, c, a = parts[0], parts[1], float(parts[2])
                        if m in self.months and c in self.categories:
                            self.sales_data[c][self.months.index(m)] += a
            self.update_chart()
            QMessageBox.information(self, "Success", "Data imported successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to parse file: {e}")

    def clear_data(self):
        for cat in self.categories:
            self.sales_data[cat] = [0.0] * 12
        self.update_chart()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SalesApp()
    window.show()
    sys.exit(app.exec())