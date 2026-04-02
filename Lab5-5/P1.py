"""
Khanon Charoenphanupong
663040475-1
P1
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QDateEdit, QSpinBox,
    QPushButton, QDialog, QMessageBox, QScrollArea,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QDate, QLocale
from PySide6.QtGui import QFont

class RoomCard(QWidget):
    room_selected = Signal(str, int)

    def __init__(self, room_name: str, price: int, description: str, emoji: str = "🏨"):
        super().__init__()
        self._is_selected = False
        self.room_name = room_name
        self.price = price

        self._build_ui(emoji, description)
        self.deselect()

    def _build_ui(self, emoji: str, description: str):
        self.setFixedSize(200, 220)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        self.emoji_lbl = QLabel(emoji)
        self.emoji_lbl.setFont(QFont("Segoe UI Emoji", 35))
        self.emoji_lbl.setAlignment(Qt.AlignCenter)

        self.name_lbl = QLabel(self.room_name)
        self.name_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.name_lbl.setAlignment(Qt.AlignCenter)

        self.price_lbl = QLabel(f"${self.price} / night")
        self.price_lbl.setAlignment(Qt.AlignCenter)
        self.price_lbl.setFont(QFont("Segoe UI", 9))

        self.desc_lbl = QLabel(description)
        self.desc_lbl.setWordWrap(True)
        self.desc_lbl.setFont(QFont("Segoe UI", 9))
        self.desc_lbl.setAlignment(Qt.AlignCenter)

        self.select_btn = QPushButton("Select Room")
        self.select_btn.clicked.connect(self._on_select_clicked)
        self.select_btn.setFixedHeight(28)

        layout.addWidget(self.emoji_lbl)
        layout.addWidget(self.name_lbl)
        layout.addWidget(self.price_lbl)
        layout.addWidget(self.desc_lbl)
        layout.addStretch()
        layout.addWidget(self.select_btn)

    def _on_select_clicked(self):
        self.room_selected.emit(self.room_name, self.price)

    def select(self):
        self._is_selected = True
        self.setStyleSheet(
            "RoomCard { background-color: #fff7ed; border: 2px solid #f97316; border-radius: 12px; }"
        )
        self.price_lbl.setStyleSheet("font-weight: bold; color: #4b5563;")
        self.desc_lbl.setStyleSheet("color: #6b7280;")
        self.select_btn.setStyleSheet(
            "background-color: #6366f1; color: white; border: none; border-radius: 6px; padding: 5px; font-weight: bold;"
        )
        self.select_btn.setText("✓ Selected")

    def deselect(self):
        self._is_selected = False
        self.setStyleSheet(
            "RoomCard { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; }"
            "RoomCard:hover { border: 2px solid #6366f1; background-color: #f5f3ff; }"
        )
        self.price_lbl.setStyleSheet("color: #4b5563;")
        self.desc_lbl.setStyleSheet("color: #9ca3af;")
        self.select_btn.setStyleSheet(
            "QPushButton { background-color: #6366f1; color: white; border: none; border-radius: 6px; padding: 5px; }"
            "QPushButton:hover { background-color: #4f46e5; }"
        )
        self.select_btn.setText("Select Room")


class ConfirmDialog(QDialog):
    def __init__(self, guest_name: str, room_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Booking Confirmed")
        self.setFixedSize(360, 240)
        self.setModal(True)
        self._build_ui(guest_name, room_name)

    def _build_ui(self, guest_name: str, room_name: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        icon = QLabel("✅")
        icon.setFont(QFont("Segoe UI Emoji", 40))
        icon.setAlignment(Qt.AlignCenter)

        title = QLabel("Booking Successful!")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #22c55e;")
        title.setAlignment(Qt.AlignCenter)

        msg = QLabel(f"Dear {guest_name},\n{room_name} is ready to welcome you! 🎉")
        msg.setAlignment(Qt.AlignCenter)
        msg.setWordWrap(True)
        msg.setFont(QFont("Segoe UI", 10))

        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(40)
        ok_btn.clicked.connect(self.accept)
        ok_btn.setStyleSheet(
            "background-color: #22c55e; color: white; border-radius: 6px; font-size: 14px; font-weight: bold;"
        )

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(msg)
        layout.addWidget(ok_btn)


class BookingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_room = None
        self.selected_price = 0
        self.cards = []
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(16)

        # --- Title ---
        title = QLabel("🏨  Book Your Stay at CozyStay")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        subtitle = QLabel("Fill in your details and choose your room")
        subtitle.setStyleSheet("color: #6b7280;")
        subtitle.setFont(QFont("Segoe UI", 10))
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # --- Guest Information Section ---
        guest_section_lbl = QLabel("🗒  Guest Information")
        guest_section_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        guest_section_lbl.setStyleSheet("color: #374151;")
        main_layout.addWidget(guest_section_lbl)

        form_frame = QFrame()
        form_frame.setStyleSheet(
            "QFrame { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; }"
        )
        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(24, 20, 24, 20)
        form_layout.setSpacing(14)
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        input_style = (
            "border: 1px solid #d1d5db; border-radius: 6px; padding: 6px 10px;"
            "background: white; font-size: 13px;"
        )
        label_style = "font-weight: bold; color: #374151; font-size: 13px;"

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. John Smith")
        self.name_input.setStyleSheet(input_style)
        self.name_input.setMinimumHeight(34)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("e.g. 081-234-5678")
        self.phone_input.setStyleSheet(input_style)
        self.phone_input.setMinimumHeight(34)

        en_locale = QLocale(QLocale.English, QLocale.UnitedStates)

        self.checkin_input = QDateEdit(QDate.currentDate())
        self.checkin_input.setCalendarPopup(True)
        self.checkin_input.setDisplayFormat("dd/MM/yyyy")
        self.checkin_input.setLocale(en_locale)
        self.checkin_input.setStyleSheet(input_style)
        self.checkin_input.setMinimumHeight(34)
        self.checkin_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.checkout_input = QDateEdit(QDate.currentDate().addDays(1))
        self.checkout_input.setCalendarPopup(True)
        self.checkout_input.setDisplayFormat("dd/MM/yyyy")
        self.checkout_input.setLocale(en_locale)
        self.checkout_input.setStyleSheet(input_style)
        self.checkout_input.setMinimumHeight(34)
        self.checkout_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.guests_input = QSpinBox()
        self.guests_input.setRange(1, 10)
        self.guests_input.setValue(1)
        self.guests_input.setSuffix(" guest(s)")
        self.guests_input.setLocale(en_locale)
        self.guests_input.setStyleSheet(input_style)
        self.guests_input.setMinimumHeight(34)
        self.guests_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        def make_label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet(label_style)
            return lbl

        form_layout.addRow(make_label("Full Name :"), self.name_input)
        form_layout.addRow(make_label("Phone Number :"), self.phone_input)
        form_layout.addRow(make_label("Check-in Date :"), self.checkin_input)
        form_layout.addRow(make_label("Check-out Date :"), self.checkout_input)
        form_layout.addRow(make_label("Guests :"), self.guests_input)

        main_layout.addWidget(form_frame)

        # --- Select a Room Section ---
        room_section_lbl = QLabel("🛏  Select a Room")
        room_section_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        room_section_lbl.setStyleSheet("color: #374151;")
        main_layout.addWidget(room_section_lbl)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)
        rooms_data = [
            ("Standard Room", 50, "Single bed, Free Wi-Fi", "🛏"),
            ("Deluxe Room", 120, "Double bed, Ocean view, Wi-Fi", "🌊"),
            ("Suite Room", 250, "Living room, Jacuzzi, Premium view", "👑"),
            ("Family Room", 160, "2 Bedrooms, Perfect for families", "👨‍👩‍👧‍👦"),
        ]

        for name, price, desc, emoji in rooms_data:
            card = RoomCard(name, price, desc, emoji)
            card.room_selected.connect(self._on_room_selected)
            self.cards.append(card)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        main_layout.addLayout(cards_layout)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        self.clear_btn = QPushButton("🗑  Clear Info")
        self.clear_btn.setFixedHeight(36)
        self.clear_btn.setStyleSheet(
            "QPushButton { background-color: #f3f4f6; color: #374151; border: 1px solid #d1d5db;"
            "border-radius: 8px; padding: 6px 16px; font-size: 13px; }"
            "QPushButton:hover { background-color: #e5e7eb; }"
        )
        self.clear_btn.clicked.connect(self.clear_form)

        self.next_btn = QPushButton("Next →")
        self.next_btn.setFixedHeight(36)
        self.next_btn.setStyleSheet(
            "background-color: #6366f1; color: white; padding: 6px 24px;"
            "border-radius: 8px; font-weight: bold; font-size: 13px;"
        )

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn)
        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

        scroll.setWidget(container)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def _on_room_selected(self, room_name: str, price: int):
        self.selected_room = room_name
        self.selected_price = price
        for card in self.cards:
            card.deselect()
            if card.room_name == room_name:
                card.select()

    def clear_form(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.checkin_input.setDate(QDate.currentDate())
        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.guests_input.setValue(1)
        self.selected_room = None
        self.selected_price = 0
        for card in self.cards:
            card.deselect()

    def get_booking_data(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        checkin = self.checkin_input.date()
        checkout = self.checkout_input.date()

        if not name or not phone:
            QMessageBox.warning(self, "Missing Information", "Please enter name and phone.")
            return None
        if checkin >= checkout:
            QMessageBox.warning(self, "Invalid Dates", "Check-out must be after check-in.")
            return None
        if not self.selected_room:
            QMessageBox.warning(self, "No Room Selected", "Please select a room.")
            return None

        nights = checkin.daysTo(checkout)
        return {
            "name": name,
            "phone": phone,
            "checkin": checkin.toString("dd/MM/yyyy"),
            "checkout": checkout.toString("dd/MM/yyyy"),
            "nights": nights,
            "guests": self.guests_input.value(),
            "room": self.selected_room,
            "price": self.selected_price,
            "total": nights * self.selected_price,
        }


class ReviewPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(16)

        title = QLabel("📋  Booking Summary")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        subtitle = QLabel("Please review your details before confirming")
        subtitle.setStyleSheet("color: #6b7280;")
        subtitle.setFont(QFont("Segoe UI", 10))
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.info_frame = QFrame()
        self.info_frame.setStyleSheet(
            "QFrame { background-color: white; border: 1px solid #e5e7eb; border-radius: 12px; }"
        )
        grid = QGridLayout(self.info_frame)
        grid.setContentsMargins(28, 20, 28, 20)
        grid.setVerticalSpacing(14)
        grid.setHorizontalSpacing(10)
        # col 0: emoji, col 1: field label, col 2: value
        grid.setColumnStretch(2, 1)

        # (emoji, label_text, key)
        field_defs = [
            ("🛏", "Room", "Room"),
            ("💰", "Price / Night", "Price / Night"),
            ("👤", "Guest Name", "Guest Name"),
            ("📞", "Phone", "Phone"),
            ("📅", "Check-in", "Check-in"),
            ("📅", "Check-out", "Check-out"),
            ("✅", "Nights", "Nights"),
            ("👥", "Guests", "Guests"),
        ]

        self.labels = {}
        emoji_font = QFont("Segoe UI Emoji", 13)
        lbl_style = "color: #6b7280; font-size: 13px;"
        val_style = "color: #111827; font-size: 13px;"

        for row, (emoji, label_text, key) in enumerate(field_defs):
            emoji_lbl = QLabel(emoji)
            emoji_lbl.setFont(emoji_font)
            emoji_lbl.setFixedWidth(26)
            emoji_lbl.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

            field_lbl = QLabel(label_text)
            field_lbl.setStyleSheet(lbl_style)
            field_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            val_lbl = QLabel("-")
            val_lbl.setStyleSheet(val_style)
            val_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.labels[key] = val_lbl

            grid.addWidget(emoji_lbl, row, 0, Qt.AlignVCenter)
            grid.addWidget(field_lbl, row, 1, Qt.AlignVCenter)
            grid.addWidget(val_lbl,   row, 2, Qt.AlignVCenter)

        layout.addWidget(self.info_frame)

        self.total_lbl = QLabel("Total Amount: $0")
        self.total_lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.total_lbl.setStyleSheet("color: #6366f1;")
        layout.addWidget(self.total_lbl, alignment=Qt.AlignRight)

        layout.addStretch()

        btns = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.setFixedHeight(36)
        self.back_btn.setStyleSheet(
            "QPushButton { background-color: #f3f4f6; color: #374151; border: 1px solid #d1d5db;"
            "border-radius: 8px; padding: 6px 16px; font-size: 13px; }"
            "QPushButton:hover { background-color: #e5e7eb; }"
        )

        self.submit_btn = QPushButton("✅  Confirm Booking")
        self.submit_btn.setFixedHeight(36)
        self.submit_btn.setStyleSheet(
            "background-color: #22c55e; color: white; padding: 6px 24px;"
            "border-radius: 8px; font-weight: bold; font-size: 13px;"
        )

        btns.addWidget(self.back_btn)
        btns.addStretch()
        btns.addWidget(self.submit_btn)
        layout.addLayout(btns)

    def load_data(self, data: dict):
        self.labels["Room"].setText(data["room"])
        self.labels["Price / Night"].setText(f"${data['price']}")
        self.labels["Guest Name"].setText(data["name"])
        self.labels["Phone"].setText(data["phone"])
        self.labels["Check-in"].setText(data["checkin"])
        self.labels["Check-out"].setText(data["checkout"])
        self.labels["Nights"].setText(f"{data['nights']} night(s)")
        self.labels["Guests"].setText(f"{data['guests']} guest(s)")
        self.total_lbl.setText(f"💳  Total Amount: ${data['total']}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CozyStay — Hotel Booking System")
        self.resize(950, 700)
        self.setStyleSheet("QMainWindow { background-color: #f9fafb; }")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.booking_page = BookingPage()
        self.review_page = ReviewPage()
        self.stack.addWidget(self.booking_page)
        self.stack.addWidget(self.review_page)

        self.booking_page.next_btn.clicked.connect(self._go_to_review)
        self.review_page.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.review_page.submit_btn.clicked.connect(self._on_submit)

        self.stack.setCurrentIndex(0)

    def _go_to_review(self):
        data = self.booking_page.get_booking_data()
        if data:
            self.review_page.load_data(data)
            self.stack.setCurrentIndex(1)

    def _on_submit(self):
        data = self.booking_page.get_booking_data()
        if data:
            dlg = ConfirmDialog(data["name"], data["room"], self)
            dlg.exec()
            self.booking_page.clear_form()
            self.stack.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())