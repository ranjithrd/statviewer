import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QListWidget

# Create a list of names
names = ["Royal Challengers", "CSK", "MI", "RR", ]

class SearchNameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Search Name Window")
        self.setGeometry(100, 100, 400, 300)

        # Create a central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

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
        # Get the selected name from the clicked item
        selected_name = item.text()
        print(f"{selected_name}")
        self.close()  # Close the window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchNameWindow()
    window.show()
    sys.exit(app.exec_())
