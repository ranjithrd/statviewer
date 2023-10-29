import pkgutil
search_path = ['.'] # set to None to see all modules importable from sys.path
all_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
print(all_modules)


import sys
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QWidget, QListWidget
from src.data.metadata import dbPlayers
from src.app.player import PlayerWindow

# Create a list of names
names = dbPlayers()

# Save selected name/s
selectedNames = []

openWindow = None

class SearchNameWindow(QWidget):

    compare = False
    secondTime = False

    def __init__(self, compare = False, secondTime = False):
        super().__init__()

        self.compare = compare
        self.secondTime = secondTime

        # Set window properties
        self.setWindowTitle("Search Name Window")
        self.setGeometry(100, 100, 400, 300)

        # Create a central widget and layout
        # central_widget = QWidget()
        # self.setCentralWidget(central_widget)
        # central_widget.setLayout(layout)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a search bar (QLineEdit)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for a name")
        layout.addWidget(self.search_bar)

        # Create a list widget to display the names
        self.list_widget = QListWidget()
        self.list_widget.addItems(names)
        layout.addWidget(self.list_widget)

        # Connect the search bar textChanged signal to update the list
        self.search_bar.textChanged.connect(self.updateList)

        # Connect itemClicked signal to return the selected name and close the window
        self.list_widget.itemClicked.connect(self.itemClicked)

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

        if not self.compare:
            openWindow = PlayerWindow(selectedNames)
            openWindow.show()
            self.close()

        # self.close()  # Close the window
