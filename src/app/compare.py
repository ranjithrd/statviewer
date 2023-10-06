import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class ComparisonWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Comparison Window")
        self.setGeometry(100, 100, 400, 150)

        # Create a central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create a label to display the text
        label = QLabel("Comparison should be based on:")
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ComparisonWindow()
    window.show()
    sys.exit(app.exec_())
