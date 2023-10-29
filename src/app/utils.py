from PySide6.QtWidgets import QApplication

def getScreenSize():
    s = QApplication.primaryScreen().availableGeometry()
    return s.width(), s.height()