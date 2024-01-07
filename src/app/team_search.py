import sys
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QWidget, QListWidget, QComboBox, QLabel, QPushButton, QHBoxLayout, QMessageBox
from src.data.metadata import dbTeams
from src.app.team import TeamWindow
from src.app.team_compare import TeamCompare
from src.app.chart import order, orderInverse
from src.constants import defaultEnd, defaultStart

# Create a list of names
names = dbTeams()

# Save selected name/s
selectedNames = []
startDates = []
endDates = []

openWindow = None

years = order.values()

class TeamSearchNameWindow(QWidget):

    compare = False
    secondTime = False
    datesRendered = False

    def __init__(self, compare = False, secondTime = False):
        global selectedNames
        super().__init__()

        self.compare = compare
        self.secondTime = secondTime

        if not secondTime:
            selectedNames = []

        # Set window properties
        self.setWindowTitle("Search Name Window")
        self.setGeometry(100, 100, 400, 300)

        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        layout = QVBoxLayout()

        if secondTime:
            layout.addWidget(QLabel("Second Name"))

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for a name")
        if secondTime:
            self.search_bar.setPlaceholderText("Search for the second name")
        layout.addWidget(self.search_bar)

        self.list_widget = QListWidget()
        self.list_widget.addItems(names)
        layout.addWidget(self.list_widget)

        # Connect the search bar textChanged signal to update the list
        self.search_bar.textChanged.connect(self.updateList)

        # Connect itemClicked signal to return the selected name and close the window
        self.list_widget.itemClicked.connect(self.itemClicked)

        self.mainLayout.addLayout(layout)

    def renderDateSelect(self):
        self.datesRendered = True
        global startDates, endDates

        self.startDate = defaultStart
        self.endDate = defaultEnd

        layout2 = QVBoxLayout()

        layout2.addWidget(QLabel("Starting Year"))
        combo_box = QComboBox()
        for i in years:
            combo_box.addItem(i)
        def s():
            self.startDate = combo_box.currentText()
        combo_box.activated.connect(s)
        layout2.addWidget(combo_box)

        combo_box.setCurrentText(defaultStart)

        layout2.addStretch(2)

        layout2.addWidget(QLabel("Ending Year"))
        combo_box2 = QComboBox()
        for i in years:
            combo_box2.addItem(i)
        def s2():
            self.endDate = combo_box2.currentText()
        combo_box2.activated.connect(s2)
        layout2.addWidget(combo_box2)

        combo_box2.setCurrentText(defaultEnd)

        layout2.addStretch(5)

        btn = QPushButton("Choose")
        btn.clicked.connect(self.submit)
        layout2.addWidget(btn)

        self.mainLayout.addLayout(layout2)

        self.startDate = defaultStart
        self.endDate = defaultEnd


    def updateList(self):
        # Get the text from the search bar
        search_text = self.search_bar.text().strip().lower()

        # Clear the list widget
        self.list_widget.clear()

        # Filter and display matching names
        if search_text:
            matching_names = [name for name in names if search_text in name.lower()]
            self.list_widget.addItems(matching_names)
        else:
            self.list_widget.addItems(names)

    def itemClicked(self, item):
        global openWindow
        
        # Get the selected name from the clicked item
        selected_name = item.text()
        selectedNames.append(selected_name)

        if not self.datesRendered:
            self.renderDateSelect()

    def submit(self):
        global openWindow, openWindow3, a
        if orderInverse[self.startDate] > orderInverse[self.endDate]:
            return
        else:
            startDates.append(self.startDate)
            endDates.append(self.endDate)
        

        if not self.compare:
            openWindow = TeamWindow(selectedNames, startDates, endDates)
            openWindow.show()
            self.close()
        else: # Compare
            if self.secondTime:
                openWindow3 = TeamCompare(selectedNames, startDates, endDates)
                openWindow3.show()
                self.close()
            else:
                # openWindow4 = SearchNameWindow(True, True)
                # openWindow4.show()
                # self.close()
                # self.mainLayout.deleteLater()
                self.close()
                a = TeamSearchNameWindowA(True, True)
                a.show()


class TeamSearchNameWindowA(TeamSearchNameWindow):
    def __init__(self, compare=False, secondTime=False):
        super().__init__(compare, secondTime)