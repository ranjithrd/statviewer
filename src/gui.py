from src.app.home import MainWindow
import sys
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)

    app.setStyleSheet("* { font-family: 'Barlow'}")

    w = MainWindow()
    w.show()
    app.exec_()
