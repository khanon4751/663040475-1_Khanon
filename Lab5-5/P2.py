"""
Khanon Charoenphanupong
663040475-1
P2
"""
"""
Student Registration System — PySide6
======================================
3 pages via QStackedWidget + Signal/Slot.

Page 1 : Card list (drag-drop reorder, delete)
Page 2 : Add student form
Page 3 : Review & confirm
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QLabel, QLineEdit, QPushButton, QComboBox, QFrame,
    QMessageBox, QDialog, QSizePolicy,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor

from data import COURSES
from style import C, BASE, INPUT_SS, COMBO_SS, SCROLL_SS
from style import btn_ss, section_label, field_label, divider
from StudentCard import StudentCard


# ─────────────────────────────────────────────────────────────
#  Page 1 — Student List
# ─────────────────────────────────────────────────────────────
class StudentListPage(QWidget):

    go_to_add = Signal()

    def __init__(self):
        super().__init__()
        self._cards: list[StudentCard] = []
        self.setAcceptDrops(True)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── top bar ──
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)

        title = QLabel("Students")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet(f"color:{C['text']};")

        self.lbl_count = QLabel("0 enrolled")
        self.lbl_count.setStyleSheet(f"color:{C['muted']}; font-size:13px;")

        btn_add = QPushButton("+ Add Student")
        btn_add.setCursor(QCursor(Qt.PointingHandCursor))
        btn_add.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        btn_add.clicked.connect(self.go_to_add.emit)

        bl.addWidget(title)
        bl.addSpacing(12)
        bl.addWidget(self.lbl_count, alignment=Qt.AlignVCenter)
        bl.addStretch()
        bl.addWidget(btn_add)

        root.addWidget(bar)

        # ── empty label ──
        self._lbl_empty = QLabel(
            "No students registered yet.\nClick \"+ Add Student\" to get started."
        )
        self._lbl_empty.setAlignment(Qt.AlignCenter)
        self._lbl_empty.setStyleSheet(f"color:{C['muted']}; font-size:13px;")
        self._lbl_empty.setVisible(True)
        root.addWidget(self._lbl_empty, stretch=1)

        # ── scroll area for cards ──
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet(SCROLL_SS)
        self._scroll.setVisible(False)

        self._container = QWidget()
        self._container.setStyleSheet(f"background:{C['bg']};")
        self._card_lay = QVBoxLayout(self._container)
        self._card_lay.setContentsMargins(24, 16, 24, 16)
        self._card_lay.setSpacing(8)
        self._card_lay.addStretch()

        self._scroll.setWidget(self._container)
        root.addWidget(self._scroll, stretch=1)

    # ── public ───────────────────────────────────────────────
    def add_student(self, data: dict):
        card = StudentCard(data)
        card.delete_requested.connect(self._remove_card)
        self._cards.append(card)
        # insert before the trailing stretch
        self._card_lay.insertWidget(self._card_lay.count() - 1, card)
        self._refresh_count()
        self._refresh_empty()

    # ── private ──────────────────────────────────────────────
    def _remove_card(self, card: StudentCard):
        reply = QMessageBox.question(
            self, "Remove student",
            f"Remove {card.data['fullname']}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self._cards.remove(card)
            self._card_lay.removeWidget(card)
            card.deleteLater()
            self._refresh_count()
            self._refresh_empty()

    def _refresh_count(self):
        n = len(self._cards)
        self.lbl_count.setText(f"{n} enrolled")

    def _refresh_empty(self):
        has = bool(self._cards)
        self._lbl_empty.setVisible(not has)
        self._scroll.setVisible(has)

    # ── drag-drop reorder ────────────────────────────────────
    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == "student_card":
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        src = event.source()
        if not isinstance(src, StudentCard) or src not in self._cards:
            return

        local_y = self._container.mapFrom(self, event.position().toPoint()).y()
        target = len(self._cards) - 1
        for i, card in enumerate(self._cards):
            if local_y < card.y() + card.height() // 2:
                target = i
                break

        src_idx = self._cards.index(src)
        if src_idx == target:
            return

        self._cards.pop(src_idx)
        self._cards.insert(target, src)
        for card in self._cards:
            self._card_lay.removeWidget(card)
        for i, card in enumerate(self._cards):
            self._card_lay.insertWidget(i, card)

        event.acceptProposedAction()


# ─────────────────────────────────────────────────────────────
#  Page 2 — Add Student Form
# ─────────────────────────────────────────────────────────────
class AddStudentPage(QWidget):

    go_back   = Signal()
    go_review = Signal(dict)

    def __init__(self):
        super().__init__()
        self._build()

    def _inp(self, ph: str = "") -> QLineEdit:
        e = QLineEdit()
        e.setPlaceholderText(ph)
        e.setMinimumHeight(38)
        e.setStyleSheet(INPUT_SS)
        return e

    def _combo(self) -> QComboBox:
        cb = QComboBox()
        cb.addItems(COURSES)
        cb.setMinimumHeight(38)
        cb.setStyleSheet(COMBO_SS)
        cb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return cb

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Add Student")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()
        root.addWidget(bar)

        # scrollable form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(SCROLL_SS)

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        # ── personal info ─────────────────────────────────────
        form.addWidget(section_label("Personal Information"))

        # grid: label | field  (label | field)
        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(12)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(3, 2)

        def flbl(text):
            l = QLabel(text)
            l.setStyleSheet(f"color:{C['text']}; font-size:13px;")
            return l

        self.inp_sid   = self._inp("e.g. 65010001")
        self.inp_first = self._inp("First name")
        self.inp_last  = self._inp("Last name")
        self.inp_fac   = self._inp("e.g. Science & Technology")
        self.inp_major = self._inp("e.g. Computer Science")

        # row 0: Student ID (spans full width via 2 cols)
        grid.addWidget(flbl("Student ID *"),  0, 0)
        grid.addWidget(self.inp_sid,          0, 1)

        # row 1: First Name | Last Name
        grid.addWidget(flbl("First Name *"),  1, 0)
        grid.addWidget(self.inp_first,        1, 1)
        grid.addWidget(flbl("Last Name *"),   1, 2)
        grid.addWidget(self.inp_last,         1, 3)

        # row 2: Faculty | Major
        grid.addWidget(flbl("Faculty *"),     2, 0)
        grid.addWidget(self.inp_fac,          2, 1)
        grid.addWidget(flbl("Major *"),       2, 2)
        grid.addWidget(self.inp_major,        2, 3)

        form.addLayout(grid)
        form.addWidget(divider())

        # ── course selection ──────────────────────────────────
        form.addWidget(section_label("Course Selection  (choose 1–3)"))

        course_grid = QGridLayout()
        course_grid.setHorizontalSpacing(16)
        course_grid.setVerticalSpacing(12)
        course_grid.setColumnStretch(1, 1)

        self.combo1 = self._combo()
        self.combo2 = self._combo()
        self.combo3 = self._combo()

        for i, (lbl_txt, cb) in enumerate([
            ("Course 1", self.combo1),
            ("Course 2", self.combo2),
            ("Course 3", self.combo3),
        ]):
            l = QLabel(lbl_txt)
            l.setStyleSheet(f"color:{C['text']}; font-size:13px;")
            l.setFixedWidth(80)
            course_grid.addWidget(l,  i, 0)
            course_grid.addWidget(cb, i, 1)

        form.addLayout(course_grid)

        # ── error label ───────────────────────────────────────
        self.lbl_err = QLabel("")
        self.lbl_err.setStyleSheet(f"color:{C['red']}; font-size:13px;")
        form.addWidget(self.lbl_err)

        form.addStretch()

        # ── buttons ───────────────────────────────────────────
        btn_row = QHBoxLayout()
        bc = QPushButton("← Cancel")
        bc.setCursor(QCursor(Qt.PointingHandCursor))
        bc.setStyleSheet(
            btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}")
        )
        bc.clicked.connect(self._on_cancel)

        br = QPushButton("Review →")
        br.setCursor(QCursor(Qt.PointingHandCursor))
        br.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        br.clicked.connect(self._on_review)

        btn_row.addWidget(bc)
        btn_row.addStretch()
        btn_row.addWidget(br)
        form.addLayout(btn_row)

        scroll.setWidget(body)
        root.addWidget(scroll, stretch=1)

    def _on_cancel(self):
        self.clear_form()
        self.go_back.emit()

    def _on_review(self):
        sid   = self.inp_sid.text().strip()
        first = self.inp_first.text().strip()
        last  = self.inp_last.text().strip()
        fac   = self.inp_fac.text().strip()
        major = self.inp_major.text().strip()

        c1 = self.combo1.currentText()
        c2 = self.combo2.currentText()
        c3 = self.combo3.currentText()

        missing = []
        if not sid:   missing.append("Student ID")
        if not first: missing.append("First Name")
        if not last:  missing.append("Last Name")
        if not fac:   missing.append("Faculty")
        if not major: missing.append("Major")

        has_course = any(
            c != "— Select Course —" for c in [c1, c2, c3]
        )
        if not has_course:
            missing.append("at least 1 course")

        if missing:
            self.lbl_err.setText("Required:  " + ",  ".join(missing))
            return

        self.lbl_err.setText("")
        data = {
            "student_id": sid,
            "fullname":   f"{first} {last}",
            "first":      first,
            "last":       last,
            "faculty":    fac,
            "major":      major,
            "course1":    c1 if c1 != "— Select Course —" else "",
            "course2":    c2 if c2 != "— Select Course —" else "",
            "course3":    c3 if c3 != "— Select Course —" else "",
        }
        self.go_review.emit(data)

    def load_data(self, d: dict):
        """Pre-fill form when user clicks Edit on Page 3."""
        self.inp_sid.setText(d.get("student_id", ""))
        self.inp_first.setText(d.get("first", ""))
        self.inp_last.setText(d.get("last", ""))
        self.inp_fac.setText(d.get("faculty", ""))
        self.inp_major.setText(d.get("major", ""))

        for combo, key in [
            (self.combo1, "course1"),
            (self.combo2, "course2"),
            (self.combo3, "course3"),
        ]:
            val = d.get(key, "")
            idx = combo.findText(val)
            combo.setCurrentIndex(idx if idx >= 0 else 0)

        self.lbl_err.setText("")

    def clear_form(self):
        for w in [self.inp_sid, self.inp_first, self.inp_last,
                  self.inp_fac, self.inp_major]:
            w.clear()
        for cb in [self.combo1, self.combo2, self.combo3]:
            cb.setCurrentIndex(0)
        self.lbl_err.setText("")


# ─────────────────────────────────────────────────────────────
#  Page 3 — Review & Confirm
# ─────────────────────────────────────────────────────────────
class ReviewConfirmPage(QWidget):

    go_edit    = Signal(dict)
    go_confirm = Signal(dict)

    def __init__(self):
        super().__init__()
        self._data: dict = {}
        self._build()

    def _row(self, layout: QVBoxLayout, label: str) -> QLabel:
        row = QHBoxLayout()
        row.setSpacing(0)
        lbl = QLabel(label)
        lbl.setFixedWidth(130)
        lbl.setStyleSheet(f"color:{C['muted']}; font-size:13px;")
        val = QLabel("—")
        val.setStyleSheet(f"color:{C['text']}; font-size:13px;")
        val.setWordWrap(True)
        row.addWidget(lbl)
        row.addWidget(val, stretch=1)
        layout.addLayout(row)
        return val

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Review & Confirm")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()
        root.addWidget(bar)

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        # ── student information ───────────────────────────────
        form.addWidget(section_label("Student Information"))

        info_box = QVBoxLayout()
        info_box.setSpacing(10)
        self.val_sid      = self._row(info_box, "Student ID")
        self.val_fullname = self._row(info_box, "Full Name")
        self.val_faculty  = self._row(info_box, "Faculty")
        self.val_major    = self._row(info_box, "Major")
        form.addLayout(info_box)

        form.addWidget(divider())

        # ── courses ───────────────────────────────────────────
        form.addWidget(section_label("Courses"))

        course_box = QVBoxLayout()
        course_box.setSpacing(10)
        self.val_c1 = self._row(course_box, "Course 1")
        self.val_c2 = self._row(course_box, "Course 2")
        self.val_c3 = self._row(course_box, "Course 3")
        form.addLayout(course_box)

        form.addStretch()

        # ── buttons ───────────────────────────────────────────
        btn_row = QHBoxLayout()
        be = QPushButton("← Edit")
        be.setCursor(QCursor(Qt.PointingHandCursor))
        be.setStyleSheet(
            btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}")
        )
        be.clicked.connect(lambda: self.go_edit.emit(self._data))

        bc = QPushButton("Confirm Registration")
        bc.setCursor(QCursor(Qt.PointingHandCursor))
        bc.setStyleSheet(btn_ss(C['green'], "#15803d"))
        bc.clicked.connect(lambda: self.go_confirm.emit(self._data))

        btn_row.addWidget(be)
        btn_row.addStretch()
        btn_row.addWidget(bc)
        form.addLayout(btn_row)

        root.addWidget(body, stretch=1)

    def load_data(self, d: dict):
        self._data = d
        self.val_sid.setText(d.get("student_id", "—"))

        fn = d.get("fullname", "")
        self.val_fullname.setText(fn)
        self.val_fullname.setStyleSheet(
            f"color:{C['accent']}; font-size:13px; font-weight:600;"
        )
        self.val_faculty.setText(d.get("faculty", "—"))
        self.val_faculty.setStyleSheet(f"color:{C['accent']}; font-size:13px;")
        self.val_major.setText(d.get("major", "—"))

        for val_lbl, key in [
            (self.val_c1, "course1"),
            (self.val_c2, "course2"),
            (self.val_c3, "course3"),
        ]:
            v = d.get(key, "")
            val_lbl.setText(v if v else "—")
            if v:
                val_lbl.setStyleSheet(f"color:{C['accent']}; font-size:13px;")
            else:
                val_lbl.setStyleSheet(f"color:{C['text']}; font-size:13px;")


# ─────────────────────────────────────────────────────────────
#  Success Dialog
# ─────────────────────────────────────────────────────────────
class SuccessDialog(QDialog):
    def __init__(self, fullname: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registration Successful")
        self.setFixedSize(340, 220)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        icon = QLabel("✅")
        icon.setFont(QFont("Segoe UI Emoji", 36))
        icon.setAlignment(Qt.AlignCenter)

        title = QLabel("Registration Successful!")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet(f"color:{C['green']};")
        title.setAlignment(Qt.AlignCenter)

        msg = QLabel(f"{fullname} has been registered.")
        msg.setAlignment(Qt.AlignCenter)
        msg.setWordWrap(True)
        msg.setStyleSheet(f"color:{C['text']}; font-size:13px;")

        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(40)
        ok_btn.clicked.connect(self.accept)
        ok_btn.setStyleSheet(
            f"background:{C['green']}; color:white; border-radius:6px;"
            "font-size:14px; font-weight:bold;"
        )

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(msg)
        layout.addWidget(ok_btn)


# ─────────────────────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration")
        self.setMinimumSize(860, 580)
        self.resize(980, 660)
        self.setStyleSheet(BASE)
        self._build()

    def _build(self):
        central = QWidget()
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        self.setCentralWidget(central)

        self.stack = QStackedWidget()
        outer.addWidget(self.stack)

        self.page_list   = StudentListPage()
        self.page_add    = AddStudentPage()
        self.page_review = ReviewConfirmPage()

        self.stack.addWidget(self.page_list)    # index 0
        self.stack.addWidget(self.page_add)     # index 1
        self.stack.addWidget(self.page_review)  # index 2

        # signals
        self.page_list.go_to_add.connect(lambda: self.stack.setCurrentIndex(1))
        self.page_add.go_back.connect(lambda: self.stack.setCurrentIndex(0))
        self.page_add.go_review.connect(self._on_go_review)
        self.page_review.go_edit.connect(self._on_go_edit)
        self.page_review.go_confirm.connect(self._on_confirm)

        self.stack.setCurrentIndex(0)

    def _on_go_review(self, data: dict):
        self.page_review.load_data(data)
        self.stack.setCurrentIndex(2)

    def _on_go_edit(self, data: dict):
        self.page_add.load_data(data)
        self.stack.setCurrentIndex(1)

    def _on_confirm(self, data: dict):
        self.page_list.add_student(data)
        self.page_add.clear_form()
        self.stack.setCurrentIndex(0)
        dlg = SuccessDialog(data["fullname"], self)
        dlg.exec()


# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())