# main.py
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt
from gui import UninformedWindow, InformedWindow
import sys


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Search Visualizer")
        self.setMinimumSize(500, 300)

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("AI Search Visualizer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 20px;")

        btn_uninformed = QPushButton("Uninformed Search")
        btn_informed = QPushButton("Informed Search")

        btn_uninformed.setMinimumHeight(40)
        btn_informed.setMinimumHeight(40)

        btn_uninformed.clicked.connect(self.open_uninformed)
        btn_informed.clicked.connect(self.open_informed)

        layout.addWidget(title)
        layout.addWidget(btn_uninformed)
        layout.addWidget(btn_informed)

        # Windows reference
        self.uninformed_window = None
        self.informed_window = None

    def open_uninformed(self):
        self.uninformed_window = UninformedWindow()
        self.uninformed_window.switch_to_menu.connect(self.show)
        self.uninformed_window.show()
        self.hide()

    def open_informed(self):
        self.informed_window = InformedWindow()
        self.informed_window.switch_to_menu.connect(self.show)
        self.informed_window.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainMenu()
    main.show()
    sys.exit(app.exec())
