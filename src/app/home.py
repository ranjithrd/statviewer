import sys

from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt
from src.app.player_search import SearchNameWindow
from src.app.team_search import TeamSearchNameWindow
from src.app.utils import getScreenSize
from src.app.dream.select import SelectWindow
from src.data.metadata import dbPlayers

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # CONFIG
        self.setWindowTitle("Criceval")
        size = getScreenSize()
        self.resize(size[0]*0.8, size[1]*0.8)

        # LAYOUT
        layout = QGridLayout()
        layout.addWidget(QWidget(), 0, 0, 15, 21)

        # RENDER
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        if len(dbPlayers()) < 10:
            print("Data not loaded!")

            l1 = QLabel("Data not loaded")
            l1.setStyleSheet("font: bold 32px;")
            layout.addWidget(l1, 0, 0)

            l1 = QLabel("Download the executable Python files to initialize database.")
            l1.setStyleSheet("font: 16px;")
            layout.addWidget(l1, 1, 0)
            
            return


        # APP NAME
        nameLabel = QLabel("Criceval")
        nameLabel.setStyleSheet("QLabel {font: bold 75px; text-align: center;}")
        layout.addWidget(nameLabel, 2, 0, 2, 21, Qt.AlignmentFlag.AlignCenter)

        # BUTTONS
        self.setStyleSheet("QGridLayout {background-color: #D9F2E6;}")
        self.setStyleSheet("QPushButton {background-color: #266346; font: bold 24px; border-width: 1px; color: white; border-color: white; border-radius: 12px;}")

        analyze_player = QPushButton("Analyze a Player")
        analyze_player.clicked.connect(self.analyzePlayerWindow)
        analyze_player.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(analyze_player, 6, 1, 2, 9)
        
        analyze_team = QPushButton("Analyze a Team")
        analyze_team.clicked.connect(self.analyzeTeamWindow)
        analyze_team.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(analyze_team, 6, 11, 2, 9)

        compare_players = QPushButton("Compare Players")
        compare_players.clicked.connect(self.comparePlayerWindow)
        compare_players.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(compare_players, 9, 1, 2, 9)

        compare_teams = QPushButton("Compare Teams")
        compare_teams.clicked.connect(self.compareTeamWindow)
        compare_teams.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(compare_teams, 9, 11, 2, 9)

        custom_team = QPushButton("Custom Team")
        custom_team.clicked.connect(self.customTeamWindow)
        custom_team.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(custom_team, 12, 1, 2, 19)

    def analyzePlayerWindow(self):
        self.w = SearchNameWindow()
        self.w.show()

    def comparePlayerWindow(self):
        self.w = SearchNameWindow(True)
        self.w.show()

    def analyzeTeamWindow(self):
        self.w = TeamSearchNameWindow()
        self.w.show()

    def compareTeamWindow(self):
        self.w = TeamSearchNameWindow(True)
        self.w.show()

    def customTeamWindow(self):
        self.w = SelectWindow()
        self.w.show()