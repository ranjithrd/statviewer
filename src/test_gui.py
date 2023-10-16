from src.app.player_search import playerSearchWindow
import sys
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    playerSearchWindow(app)
    sys.exit(app.exec_())