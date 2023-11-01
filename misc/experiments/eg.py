
# importing the required libraries
  
from PySide6.QtCore import * 
from PySide6.QtGui import * 
from PySide6.QtWidgets import * 
import sys
  
  
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        layout1.setContentsMargins(0,0,0,0)
        layout1.setSpacing(20)

        layout2.addWidget(QColor('red'))
        layout2.addWidget(QColor('yellow'))
        layout2.addWidget(QColor('purple'))

        layout1.addLayout( layout2 )

        layout1.addWidget(QColor('green'))

        layout3.addWidget(QColor('red'))
        layout3.addWidget(QColor('purple'))

        layout1.addLayout( layout3 )

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
