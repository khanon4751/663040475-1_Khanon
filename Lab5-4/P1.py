"""
Khanon Charoenphanupong
663040475-1
P1
"""

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
                               QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton,
                               QFrame, QSpinBox, QColorDialog, QFileDialog, QToolBar,
                               QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction, QIcon, QPixmap
import sys, os
import pyperclip

default_color = "#B0E0E6"

class PersonalCard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Personal Info Card")
        self.setGeometry(100, 100, 450, 550)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # input section
        self.input_layout = QFormLayout()
        self.input_layout.setVerticalSpacing(12)
        self.create_form()

        self.main_layout.addSpacing(10)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(line)

        self.main_layout.addSpacing(10)

        # output section
        self.bg_widget = QWidget()
        self.output_layout = QVBoxLayout(self.bg_widget)
        self.create_display()
        self.main_layout.addWidget(self.bg_widget)

        # menu / toolbar / statusbar
        self.create_menu()
        self.create_toolbar()
        self.statusBar().showMessage("Fill in your details and click generate")

    # ---------------- FORM ----------------
    def create_form(self):
        self.name = QLineEdit()
        self.name.setPlaceholderText("First name and Lastname")

        self.age = QSpinBox()
        self.age.setRange(1,120)
        self.age.setValue(25)

        self.email = QLineEdit()
        self.email.setPlaceholderText("username@domain.name")

        self.position = QComboBox()
        self.position.addItems(["Teaching Staff","Supporting Staff","Student","Visitor"])
        self.position.setCurrentIndex(-1)
        self.position.setPlaceholderText("Choose your position")

        color_row = QWidget()
        color_layout = QHBoxLayout(color_row)
        self.fav_color = QColor(default_color)
        self.color_swatch = QLabel()
        self.color_swatch.setFixedSize(22, 22)
        self.color_swatch.setStyleSheet(f"background-color:{default_color}; border:1px solid #888;")
        color_layout.addWidget(self.color_swatch)

        color_button = QPushButton("Pick New Color")
        color_button.clicked.connect(self.pick_color)
        color_layout.addWidget(color_button)

        self.input_layout.addRow("Full name:", self.name)
        self.input_layout.addRow("Age:", self.age)
        self.input_layout.addRow("Email:", self.email)
        self.input_layout.addRow("Position:", self.position)
        self.input_layout.addRow("Your favorite color:", color_row)

        self.main_layout.addLayout(self.input_layout)

    def pick_color(self):
        color = QColorDialog.getColor(self.fav_color, self, "Pick a Color")
        if color.isValid():
            self.fav_color = color
            self.color_swatch.setStyleSheet(f"background-color:{color.name()}; border:1px solid #888;")
            self.bg_widget.setStyleSheet(f"background-color:{color.name()}; border-radius:6px;")

    # ---------------- DISPLAY ----------------
    def create_display(self):
        self.bg_widget.setStyleSheet("background-color:#B0E0E6; border-radius:6px; padding:12px;")

        self.name_label = QLabel("Your name here")
        self.name_label.setStyleSheet("font-size:18pt; font-weight:bold;")

        self.age_label = QLabel("(Age)")
        self.position_label = QLabel("Your position here")
        self.position_label = QLabel("Your position here")
        self.position_label.setStyleSheet("font-size:16pt;")

        self.email_label = QLabel()
        self.email_label.setText(
        '<img src="mail.png" width="16" height="16"> '
        'your_username@domain.name'
    )
        self.email_label.setAlignment(Qt.AlignLeft)

        self.output_layout.addWidget(self.name_label, alignment=Qt.AlignLeft)
        self.output_layout.addWidget(self.age_label, alignment=Qt.AlignLeft)
        self.output_layout.addWidget(self.position_label, alignment=Qt.AlignLeft)
        self.output_layout.addWidget(self.email_label, alignment=Qt.AlignLeft)

    # ---------------- LOGIC ----------------
    def update_display(self):
        if self.name.text().strip() == "":
            QMessageBox.warning(self, "Input Error", "Please enter your name!")
            return 
        self.name_label.setText(self.name.text())
        self.age_label.setText(f"({self.age.value()})")
        self.position_label.setText(self.position.currentText())

        self.email_label.setText(
        f'<img src="mail.png" width="16" height="16"> {self.email.text()}'
        )

        self.bg_widget.setStyleSheet(f"background-color:{self.fav_color.name()}; border-radius:6px; padding:12px;")

        self.statusBar().showMessage("Card generated")

    def clear_form(self):
        self.name.clear()
        self.age.setValue(25)
        self.email.clear()
        self.position.setCurrentIndex(-1)
        self.fav_color = QColor(default_color)
        self.color_swatch.setStyleSheet(f"background-color:{default_color}; border:1px solid #888;")
        self.statusBar().showMessage("Form cleared")

    def clear_display(self):
        self.name_label.setText("Your name here")
        self.age_label.setText("(Age)")
        self.position_label.setText("Your position here")
        self.email_label.setText(
        '<img src="mail.png" width="16" height="16"> your_username@domain.name'
    )
        self.bg_widget.setStyleSheet("background-color:#B0E0E6; border-radius:6px; padding:12px;")
        self.statusBar().showMessage("Display cleared")

    def clear_all(self):
        self.clear_form()
        self.clear_display()
        self.statusBar().showMessage("Form and display cleared")

    def save_card(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Card", "my_card.txt", "Text Files (*.txt)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"{self.name_label.text()}\n")
                f.write(f"{self.age_label.text()}\n")
                f.write(f"{self.position_label.text()}\n")
                f.write(f"{self.email_label.text()}\n")
            self.statusBar().showMessage(f"Saved card to {filename}")

    def copy_card(self):
        text = f"{self.name_label.text()}\n{self.age_label.text()}\n{self.position_label.text()}\n{self.email_label.text()}"
        pyperclip.copy(text)
        self.statusBar().showMessage("Card copied to clipboard")

    # ---------------- MENU ----------------
    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")

        generate_action = QAction("Generate Card", self)
        save_action = QAction("Save Card", self)
        clear_display_action = QAction("Clear Display", self)
        exit_action = QAction("Exit", self)

        copy_action = QAction("Copy Card", self)
        clear_form_action = QAction("Clear Form", self)

        generate_action.triggered.connect(self.update_display)
        save_action.triggered.connect(self.save_card)
        clear_display_action.triggered.connect(self.clear_display)
        exit_action.triggered.connect(self.close)

        copy_action.triggered.connect(self.copy_card)
        clear_form_action.triggered.connect(self.clear_form)

        file_menu.addAction(generate_action)
        file_menu.addAction(save_action)
        file_menu.addAction(clear_display_action)
        file_menu.addAction(exit_action)

        edit_menu.addAction(copy_action)
        edit_menu.addAction(clear_form_action)

    # ---------------- TOOLBAR ----------------
    def create_toolbar(self):
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)

        gen_action = QAction(QIcon("generate.png"), "Generate Card", self)
        save_action = QAction(QIcon("save.png"), "Save Card", self)
        clear_action = QAction(QIcon("clear.png"), "Clear All", self)

        gen_action.triggered.connect(self.update_display)
        save_action.triggered.connect(self.save_card)
        clear_action.triggered.connect(self.clear_all)

        toolbar.addAction(gen_action)
        toolbar.addAction(save_action)
        toolbar.addAction(clear_action)


def main():
    app = QApplication(sys.argv)

    if os.path.exists("P1_style.qss"):
        with open("P1_style.qss","r") as f:
            app.setStyleSheet(f.read())

    window = PersonalCard()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()