from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget, QLineEdit, QGridLayout, QWidget, QListWidget, QLabel, QPushButton, QScrollArea, QFrame, QButtonGroup, QVBoxLayout
from src.aggregate.data_points import dataPointsWhere

class ChartDataPoints(QWidget):
    def __init__(self, aggregate, dataPoints):
        super().__init__()

        self.aggregate = aggregate
        self.dataPoints = dataPoints

        self.renderCharts()

    def renderCharts(self):
        chartScrollLayout = QVBoxLayout()

        # Chart Widgets
        for k in self.dataPoints:
            i = self.dataPoints[k]
            if i[1] == True: # Should be rendered

                # SINGLE DATA POINT
                if i[3] == "single":
                    dpLayout = QVBoxLayout()

                    title = QLabel(k)
                    description = QLabel(self.aggregate[k])

                    

        chartInner = QWidget()
        chartInner.setLayout(chartScrollLayout)

        self.chartScroll = QScrollArea()
        self.chartScroll.setWidgetResizable(True)
        self.chartScroll.setWidget(chartInner)
