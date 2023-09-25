import sys
# import data
from PySide6.QtWidgets import QApplication, QPushButton, QDialog, QLineEdit, QVBoxLayout
from PySide6.QtCore import Slot

class FormDialog(QDialog):

    @Slot()
    def onSubmitClicked(self):
        print("Hello,", self.nameInput.text())

    def __init__(self, parent=None):
        super(FormDialog, self).__init__(parent)
        self.setWindowTitle("Form Dialog")

        self.nameInput = QLineEdit("Enter your name...")
        self.submitButton = QPushButton(text="Greet")

        self.submitButton.clicked.connect(self.onSubmitClicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.submitButton)

        self.setLayout(layout)

if __name__ == "__main__":
    #data.connectToDatabase(host="localhost", user="root", password="mysql123", database="pyproj")

    app = QApplication(sys.argv)
    
    form = FormDialog()
    form.show()

    sys.exit(app.exec())