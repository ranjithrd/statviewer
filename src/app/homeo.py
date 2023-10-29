import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from src.app.player_search import SearchNameWindow

class HomeWindow(QMainWindow):
    app = None

    def __init__(self, app):
        super().__init__()

        self.app = app

        # Set window properties
        self.setWindowTitle("Button Window")
        self.setGeometry(100, 100, 400, 300)

        # Create a central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create buttons
        analyze_player_button = QPushButton("Analyze a player")
        analyze_team_button = QPushButton("Analyze a team")
        compare_teams_button = QPushButton("Compare Teams")
        compare_players_button = QPushButton("Compare players")
        dream_team_button = QPushButton("Dream Team")

        # Add buttons to the layout
        layout.addWidget(analyze_player_button)
        layout.addWidget(analyze_team_button)
        layout.addWidget(compare_teams_button)
        layout.addWidget(compare_players_button)
        layout.addWidget(dream_team_button)

        # Connect button clicks to a custom slot
        analyze_player_button.clicked.connect(self.analyze_player)
        analyze_team_button.clicked.connect(self.buttonClicked)
        compare_teams_button.clicked.connect(self.buttonClicked)
        compare_players_button.clicked.connect(self.buttonClicked)
        dream_team_button.clicked.connect(self.buttonClicked)

    def analyze_player(self):
        w = SearchNameWindow()
        print(w)
        w.show()

    def buttonClicked(self):
        sender = self.sender()  # Get the button that was clicked
        button_name = sender.text()  # Get the text of the button
        print(f'{button_name}')
        self.close()  # Close the window

def showHomeWindow():
    app = QApplication(sys.argv)
    window = HomeWindow(app)
    window.show()
    app.exec_()
