import sys
import matplotlib.pyplot as plt
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel

# Predefined data (Replace this with your data)
player_data = {
    1: [10, 15, 12, 14, 18],
    2: [12, 14, 11, 13, 17],
    3: [11, 13, 10, 12, 16],
    # Add more player numbers and data as needed
}

team_data = {
    1: [10, 15, 12, 14, 18],
    2: [12, 14, 11, 13, 17],
    3: [11, 13, 10, 12, 16],
    # Add more player numbers and data as needed
}
class PlayerAnalysisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Player Analysis")
        self.setGeometry(100, 100, 800, 600)

        self.search_label = QLabel("Enter Player Number:")
        self.search_bar = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_player)

        self.plot_button = QPushButton("Plot Graph")
        self.plot_button.clicked.connect(self.plot_graph)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.search_label)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.plot_button)
        self.setLayout(self.layout)

        self.player_number = None

    def search_player(self):
        try:
            self.player_number = int(self.search_bar.text())
        except ValueError:
            self.player_number = None

    def plot_graph(self):
        if self.player_number is not None:
            player_data_list = player_data.get(self.player_number, [])
            if player_data_list:
                plt.plot(player_data_list)
                plt.xlabel("Match Number")
                plt.ylabel("Score")
                plt.title(f"Player {self.player_number} Performance")
                plt.show()
                
class TeamAnalysisWindow(QWidget):
    def __init__(self, team_name):
        super().__init__()
        self.setWindowTitle(f"Team Analysis - {team_name}")
        self.setGeometry(100, 100, 800, 600)

        # Add the widgets and functionality for team analysis here
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Player Analysis App")
        self.setGeometry(100, 100, 400, 300)

        analyze_team_button = QPushButton("Analyze a Team")
        analyze_team_button.clicked.connect(self.open_team_analysis_window)

        analyze_player_button = QPushButton("Analyze a Player")
        analyze_player_button.clicked.connect(self.open_player_analysis_window)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(analyze_team_button)
        layout.addWidget(analyze_player_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_team_analysis_window(self):
        team_names = list(team_data.keys())
        team_analysis_window = TeamAnalysisWindow(team_names[0])
        team_analysis_window.show()

    def open_player_analysis_window(self):
        player_analysis_window = PlayerAnalysisWindow()
        player_analysis_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
