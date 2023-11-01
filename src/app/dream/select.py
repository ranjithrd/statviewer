from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QGridLayout, QComboBox, QListWidget
from PySide6.QtCore import Qt
from src.data.metadata import dbPlayers
from src.app.dream.dream_compare import DreamCompareWindow

class SelectWindow(QMainWindow):
    def __init__(self):
        super(SelectWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Player Search")
        self.setGeometry(250, 250, 800, 1000)

        self.lst_play = dbPlayers()

        # Create 22 boxes (buttons in this case)
        self.boxes = [QPushButton(f"Click to place", self) for i in range(22)]
        for box in self.boxes:
            box.setCheckable(True)
            box.clicked.connect(self.box_clicked)

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(QLabel("Team 1"), 0, 0)
        self.grid_layout.addWidget(QLabel("Team 2"), 0, 1)
        for index, box in enumerate(self.boxes):
            row = index % 11
            col = index // 11
            self.grid_layout.addWidget(box, row+1, col)

        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(QLabel("Search and choose a player above and then select a slot to add them to"))
        self.central_layout.addStretch(2)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for a name")
        self.central_layout.addWidget(self.search_bar)

        self.list_widget = QListWidget()
        self.list_widget.addItems(self.lst_play)
        self.central_layout.addWidget(self.list_widget)

        self.search_bar.textChanged.connect(self.updateList)
        self.list_widget.itemClicked.connect(self.itemClicked)

        self.central_layout.addStretch(3)
        self.central_layout.addLayout(self.grid_layout)
        self.central_layout.addStretch(3)
        
        btn = QPushButton("Compare")
        btn.clicked.connect(self.onCompare)
        self.central_layout.addWidget(btn)

        central_widget = QWidget(self)
        central_widget.setLayout(self.central_layout)
        self.setCentralWidget(central_widget)

    def updateList(self):
        search_text = self.search_bar.text().strip().lower()
        self.list_widget.clear()

        if search_text:
            matching_names = [name for name in self.lst_play if search_text in name.lower()]
            self.list_widget.addItems(matching_names)
        else:
            self.list_widget.addItems(self.lst_play)

    def itemClicked(self, item):
        self.selectedPlayer = item.text()

    def search_player(self):
        query = self.search_bar.text().lower()
        for box in self.boxes:
            if query in box.text().lower():
                box.setStyleSheet("background-color: yellow")
            else:
                box.setStyleSheet("")

    def box_clicked(self):
        clicked_button = self.sender()
        # Deselect other boxes
        for box in self.boxes:
            if box != clicked_button:
                box.setChecked(False)
        # If a player is being searched for, set it to the box
        # query = self.dropdown.currentText()
        query = self.selectedPlayer
        if query in self.lst_play:
            clicked_button.setText(query)

    def onCompare(self):
        team1, team2 = [], []
        for i, btn in enumerate(self.boxes):
            if btn.text() in self.lst_play:
                if i / 11 >= 1:
                    team2.append(btn.text())
                else:
                    team1.append(btn.text())

        global dreamCompareWindow
        dreamCompareWindow = DreamCompareWindow(team1, team2)
        dreamCompareWindow.show()

        self.destroy()

