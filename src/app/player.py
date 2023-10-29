from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QWidget, QListWidget, QLabel, QPushButton
from src.data.metadata import dbPlayers

class PlayerWindow(QWidget):
    selectedName = ""

    def __init__(self, selectedNames):
        super().__init__()

        self.selectedName = selectedNames[0]

        # Set window properties
        self.setWindowTitle("Comparison Window")
        self.setGeometry(100, 100, 400, 150)

        # Create a central widget and layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a label to display the text
        label = QLabel(self.selectedName)
        layout.addWidget(label)

        # Create buttons
        batting_button = QPushButton("Batting")
        bowling_button = QPushButton("Bowling")

        # Add buttons to the layout
        layout.addWidget(batting_button)
        layout.addWidget(bowling_button)

        # Connect button clicks to a custom slot
        batting_button.clicked.connect(self.buttonClicked)
        bowling_button.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        sender = self.sender()  # Get the button that was clicked
        button_name = sender.text()  # Get the text of the button
        print(f'{button_name}')
        self.close()  # Close the window
