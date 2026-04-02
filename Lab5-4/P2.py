"""
Khanon Charoenphanupong
663040475-1
P2
"""

import sys, random
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt

SLIDER_STYLE = """
QSlider::groove:horizontal {
    height: 6px;
    background: #dcdcdc;
    border-radius: 3px;
}
QSlider::sub-page:horizontal {
    background: #1e90ff;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #1e90ff;
    width: 14px;
    height: 14px;
    margin: -4px 0;
    border-radius: 7px;
}
"""

class CharacterBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Character Builder")
        self.resize(860, 520)

        self.initUI()
        self.createMenu()
        self.createToolbar()
        self.createStatusBar()

    def initUI(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # ===== LEFT PANEL =====
        left = QWidget()
        left_layout = QVBoxLayout(left)

        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter character name...")

        self.race_combo = QComboBox()
        self.race_combo.addItems(["Choose race","Human","Elf","Dwarf","Orc","Undead"])

        self.class_combo = QComboBox()
        self.class_combo.addItems(["Choose class","Warrior","Mage","Rogue","Paladin","Ranger"])

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Choose gender","Male","Female","Other"])

        form.addRow("Character Name:", self.name_edit)
        form.addRow("Race:", self.race_combo)
        form.addRow("Class:", self.class_combo)
        form.addRow("Gender:", self.gender_combo)

        left_layout.addLayout(form)
        left_layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))

        title = QLabel("Stat Allocation")
        title.setStyleSheet("color:#6a5acd; font-weight:bold;")
        left_layout.addWidget(title)

        self.sliders = {}
        self.value_labels = {}

        icons = {"STR":"⚔", "DEX":"🏹", "INT":"🔮", "VIT":"❤"}

        for stat in ["STR","DEX","INT","VIT"]:
            row = QHBoxLayout()

            icon = QLabel(icons[stat])
            label = QLabel(stat)

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(1,20)
            slider.setValue(5)
            slider.setStyleSheet(SLIDER_STYLE)

            value_label = QLabel("5")

            slider.valueChanged.connect(lambda v, l=value_label: l.setText(str(v)))
            slider.valueChanged.connect(self.updateTotal)

            row.addWidget(icon)
            row.addWidget(label)
            row.addWidget(slider)
            row.addWidget(value_label)

            left_layout.addLayout(row)

            self.sliders[stat] = slider
            self.value_labels[stat] = value_label

        self.total_label = QLabel("Points used: 20 / 40")
        left_layout.addWidget(self.total_label)

        self.generate_btn = QPushButton("⚔ Generate Character Sheet")
        self.generate_btn.setStyleSheet("""
            QPushButton{
                border:1px solid #7f7fff;
                border-radius:6px;
                padding:6px;
                color:#4b0082;
            }
        """)
        self.generate_btn.clicked.connect(self.generateSheet)
        left_layout.addWidget(self.generate_btn)

        # ===== RIGHT PANEL =====
        self.right = QWidget()
        self.right.setFixedWidth(250)
        self.right.setStyleSheet("""
            QWidget{
                background:qlineargradient(
                    x1:0,y1:0,x2:0,y2:1,
                    stop:0 #2a2a44,
                    stop:1 #171726
                );
                color:white;
                border-radius:12px;
            }
        """)
        right_layout = QVBoxLayout(self.right)

        self.sheet_title = QLabel("— Character Name —")
        self.sheet_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sheet_title.setStyleSheet("color:#cfa8ff; font-size:16px;")

        self.sheet_sub = QLabel("Race • Class")
        self.sheet_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        right_layout.addWidget(self.sheet_title)
        right_layout.addWidget(self.sheet_sub)
        right_layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))

        self.bars = {}
        for stat in ["STR","DEX","INT","VIT"]:
            lbl = QLabel(stat)
            bar = QProgressBar()
            bar.setRange(0,20)
            bar.setValue(5)
            bar.setTextVisible(False)
            bar.setStyleSheet("""
                QProgressBar{
                    background:#2b2b3c;
                    height:10px;
                    border-radius:5px;
                }
                QProgressBar::chunk{
                    background:#1e90ff;
                }
            """)
            right_layout.addWidget(lbl)
            right_layout.addWidget(bar)
            self.bars[stat] = bar

        right_layout.addStretch()

        main_layout.addWidget(left)
        main_layout.addWidget(self.right)

        self.updateTotal()

    # ===== MENU =====
    def createMenu(self):
        menubar = self.menuBar()

        game = menubar.addMenu("Game")
        game.addAction("New Character", self.newCharacter)
        game.addAction("Generate Sheet", self.generateSheet)
        game.addAction("Save Sheet", self.saveSheet)
        game.addAction("Exit", self.close)

        edit = menubar.addMenu("Edit")
        edit.addAction("Reset Stats", self.resetStats)
        edit.addAction("Randomize", self.randomize)

    # ===== TOOLBAR =====
    def createToolbar(self):
        toolbar = self.addToolBar("Toolbar")

        new_action = QAction("🆕 New", self)
        gen_action = QAction("⚔ Generate", self)
        rand_action = QAction("🎲 Randomize", self)
        save_action = QAction("💾 Save", self)

        new_action.triggered.connect(self.newCharacter)
        gen_action.triggered.connect(self.generateSheet)
        rand_action.triggered.connect(self.randomize)
        save_action.triggered.connect(self.saveSheet)

        toolbar.addAction(new_action)
        toolbar.addAction(gen_action)
        toolbar.addAction(rand_action)
        toolbar.addAction(save_action)

    # ===== STATUS BAR =====
    def createStatusBar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready — create your character")

    # ===== LOGIC =====
    def updateTotal(self):
        total = sum(s.value() for s in self.sliders.values())
        self.total_label.setText(f"Points used: {total} / 40")
        if total > 40:
            self.total_label.setStyleSheet("color:red;")
        else:
            self.total_label.setStyleSheet("color:black;")

    def validate(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self,"Error","Please enter character name.")
            return False
        if self.race_combo.currentIndex()==0:
            QMessageBox.warning(self,"Error","Please choose race.")
            return False
        if self.class_combo.currentIndex()==0:
            QMessageBox.warning(self,"Error","Please choose class.")
            return False
        if sum(s.value() for s in self.sliders.values())>40:
            QMessageBox.warning(self,"Error","Total points must not exceed 40.")
            return False
        return True

    def generateSheet(self):
        if not self.validate():
            return
        self.sheet_title.setText(f"— {self.name_edit.text()} —")
        self.sheet_sub.setText(f"{self.race_combo.currentText()} • {self.class_combo.currentText()}")
        for stat in self.sliders:
            self.bars[stat].setValue(self.sliders[stat].value())
        self.status.showMessage("Character sheet generated.",3000)

    def saveSheet(self):
        file,_ = QFileDialog.getSaveFileName(self,"Save Sheet","","Text Files (*.txt)")
        if file:
            with open(file,"w",encoding="utf-8") as f:
                f.write(self.sheet_title.text()+"\n")
                f.write(self.sheet_sub.text()+"\n")
                for s in self.sliders:
                    f.write(f"{s}: {self.sliders[s].value()}\n")
            self.status.showMessage("Saved successfully.",3000)

    def resetStats(self):
        for s in self.sliders.values():
            s.setValue(5)
        self.status.showMessage("Stats reset.",3000)

    def newCharacter(self):
        self.name_edit.clear()
        self.race_combo.setCurrentIndex(0)
        self.class_combo.setCurrentIndex(0)
        self.gender_combo.setCurrentIndex(0)
        self.resetStats()
        self.sheet_title.setText("— Character Name —")
        self.sheet_sub.setText("Race • Class")
        for b in self.bars.values():
            b.setValue(5)
        self.status.showMessage("New character.",3000)

    def randomize(self):
        while True:
            vals = [random.randint(1,20) for _ in range(4)]
            if sum(vals)<=40:
                break
        for stat,val in zip(self.sliders,vals):
            self.sliders[stat].setValue(val)
        self.name_edit.setText("Random Hero")
        self.race_combo.setCurrentIndex(random.randint(1,5))
        self.class_combo.setCurrentIndex(random.randint(1,5))
        self.gender_combo.setCurrentIndex(random.randint(1,3))
        self.status.showMessage("Randomized.",3000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CharacterBuilder()
    w.show()
    sys.exit(app.exec())