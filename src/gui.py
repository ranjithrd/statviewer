from src.app.home import MainWindow
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

def main():
    app = QApplication(sys.argv)

    QFontDatabase.addApplicationFont("fonts/Barlow-Regular.ttf")
    QFontDatabase.addApplicationFont("fonts/Barlow-Medium.ttf")
    QFontDatabase.addApplicationFont("fonts/Barlow-Bold.ttf")
    
    app.setApplicationName("Criceval")

    app.setStyleSheet("* { font-family: 'Barlow'}")

    w = MainWindow()
    w.show()
    app.exec_()
