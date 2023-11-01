import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout

class CricketAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cricket Analyser")
        self.setGeometry(100, 100, 400, 300)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Title Label
        title_label = QPushButton("Cricket Analyser")
        title_label.setEnabled(False)
        layout.addWidget(title_label)

        # Button Grid
        button_grid_layout = QHBoxLayout()
        layout.addLayout(button_grid_layout)

        # Create four buttons in a grid
        for i in range(4):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.open_new_window)
            button_grid_layout.addWidget(button)

        # Create a fifth button below the grid
        fifth_button = QPushButton("Button 5")
        fifth_button.clicked.connect(self.open_new_window)
        layout.addWidget(fifth_button)

    def open_new_window(self):
        # Function to open a new window when a button is clicked
        new_window = QMainWindow()
        new_window.setWindowTitle("New Window")
        new_window.setGeometry(200, 200, 400, 200)

        new_widget = QWidget()
        new_window.setCentralWidget(new_widget)

        new_layout = QVBoxLayout()
        new_widget.setLayout(new_layout)

        new_label = QPushButton("This is a new window.")
        new_layout.addWidget(new_label)

        new_window.show()


def main():
    app = QApplication(sys.argv)
    window = CricketAnalyzerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()





# code 2
