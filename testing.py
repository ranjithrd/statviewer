import sys
from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")  # Set the backend explicitly

class MatplotlibLineGraph(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create a Matplotlib Figure
        self.figure = Figure()

        # Create a FigureCanvas to embed the Matplotlib figure in a PySide6 widget
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)

        # Create a Matplotlib axes within the figure
        self.axes = self.figure.add_subplot(111)

        # Generate some example data and plot a line graph
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.axes.plot(x, y)

        self.setLayout(layout)

# class MPLGraphWrapper(QFrame):
#     def __init__(self, sr):
#         super().__init__()

#         central_widget = MatplotlibLineGraph(sr)
#         self.setWidget



def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Matplotlib Line Graph in PySide6")

    central_widget = MatplotlibLineGraph()
    window.setLayout(l)

    window.setGeometry(100, 100, 800, 600)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
