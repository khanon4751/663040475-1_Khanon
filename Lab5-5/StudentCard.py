"""
Khanon Charoenphanupong
663040475-1
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame,
)
from PySide6.QtCore import Qt, Signal, QMimeData, QPoint
from PySide6.QtGui import QFont, QCursor, QDrag, QPixmap

from style import C


class StudentCard(QFrame):

    delete_requested = Signal(object)  # emits self

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        self._drag_start: QPoint | None = None
        self.setAcceptDrops(False)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        self._build()

    def _build(self):
        courses = [c for c in [
            self.data.get("course1", ""),
            self.data.get("course2", ""),
            self.data.get("course3", ""),
        ] if c and c != "— Select Course —"]

        self.setMinimumHeight(70 + len(courses) * 20)
        self.setStyleSheet(f"""
            StudentCard {{
                background:{C['card']};
                border-radius: 0px;
            }}
            StudentCard:hover {{
                background:{C['surface']};
            }}
        """)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(12, 10, 12, 10)
        outer.setSpacing(8)

        # drag handle
        handle = QLabel("⠿")
        handle.setFixedWidth(16)
        handle.setAlignment(Qt.AlignTop)
        handle.setStyleSheet(
            f"background:transparent; color:{C['muted']}; font-size:18px; padding-top:2px;"
        )
        outer.addWidget(handle, alignment=Qt.AlignTop)

        # content
        content = QVBoxLayout()
        content.setSpacing(2)

        # row 1: fullname + student id
        name_row = QHBoxLayout()
        name_lbl = QLabel(self.data.get("fullname", ""))
        name_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        name_lbl.setStyleSheet(f"color:{C['text']}; background:transparent;")

        sid_lbl = QLabel(self.data.get("student_id", ""))
        sid_lbl.setStyleSheet(f"color:{C['muted']}; font-size:12px; background:transparent;")

        name_row.addWidget(name_lbl)
        name_row.addSpacing(8)
        name_row.addWidget(sid_lbl)
        name_row.addStretch()
        content.addLayout(name_row)

        # row 2: faculty · major
        dept_lbl = QLabel(
            f"{self.data.get('faculty', '')}  ·  {self.data.get('major', '')}"
        )
        dept_lbl.setStyleSheet(f"color:{C['muted']}; font-size:12px; background:transparent;")
        content.addWidget(dept_lbl)

        # courses
        for c in courses:
            c_lbl = QLabel(c)
            c_lbl.setStyleSheet(f"color:{C['text']}; font-size:12px; background:transparent;")
            content.addWidget(c_lbl)

        outer.addLayout(content)
        outer.addStretch()

        # delete button
        btn_del = QPushButton("✕")
        btn_del.setFixedSize(28, 28)
        btn_del.setCursor(QCursor(Qt.PointingHandCursor))
        btn_del.setStyleSheet(f"""
            QPushButton {{
                background:transparent;
                color:{C['muted']};
                border:none;
                border-radius:14px;
                font-size:11px;
                font-weight:bold;
            }}
            QPushButton:hover {{
                background:{C['red']};
                color:white;
                border:none;
            }}
        """)
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self))
        outer.addWidget(btn_del, alignment=Qt.AlignTop)

    # ── Drag support ──────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self._drag_start is not None:
            if (event.pos() - self._drag_start).manhattanLength() > 10:
                drag = QDrag(self)
                mime = QMimeData()
                mime.setText("student_card")
                drag.setMimeData(mime)

                pix = QPixmap(self.size())
                pix.fill(Qt.transparent)
                self.render(pix)
                drag.setPixmap(pix)
                drag.setHotSpot(event.pos())
                drag.exec(Qt.MoveAction)
        super().mouseMoveEvent(event)