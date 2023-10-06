import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Home Screen")

        button = QPushButton("Press Me!")
        button.setFixedSize(QSize(100,50))
       
        self.setFixedSize(QSize(1200, 700))
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        # Set the central widget of the Window.
        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        print("Clicked!")

       

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
