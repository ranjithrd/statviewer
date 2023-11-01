from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget, QLineEdit, QGridLayout, QWidget, QListWidget, QLabel, QPushButton, QScrollArea, QFrame, QButtonGroup, QVBoxLayout
from src.aggregate.data_points import dataPointsWhere
import pyqtgraph as pg

order = {
    1: "2007/08",
    2: "2009",
    3: "2009/10",
    4: "2011",
    5: "2012",
    6: "2013",
    7: "2014",
    8: "2015",
    9: "2016",
    10: "2017",
    11: "2018",
    12: "2019",
    13: "2020/21",
    14: "2021",
    15: "2022",
    16: "2023"
}

orderInverse = {}
for i, j in order.items():
    orderInverse[j] = i

split_seasons_convert_to = {
    1: 2007,
    2: 2009,
    3: 2010,
    4: 2011,
    5: 2012,
    6: 2013,
    7: 2014,
    8: 2015,
    9: 2016,
    10: 2017,
    11: 2018,
    12: 2019,
    13: 2020,
    14: 2021,
    15: 2022,
    16: 2023
}

class W(QWidget):
    def __init__(self, x, y, isBar=False):
        super().__init__()

        lastValue = y[-1]
        lastUniqueValue = len(y) - 1
        for i in range(len(y) - 1, 1, -1):
            if y[i] == lastValue:
                lastUniqueValue -= 1

        y = y[0:lastUniqueValue+2]
        x = x[0:lastUniqueValue+2]

        graph = pg.PlotWidget(background=None)
        graph.plotItem.showGrid(True, True, 0.3)
        if isBar:
            bar = pg.BarGraphItem(x = range(len(y)), height = y, width = 0.4)
            graph.addItem(bar)
            ticks = []
            for i in range(len(x)):
                item = x[i]
                ticks.append((i + 1, item))
            graph.plotItem.getAxis("bottom").setTicks([ticks])
        else:
            graph.plotItem.plot(x, y, pen=pg.mkPen("green", width=5))
        self.setMinimumHeight(300)
        self.setMinimumWidth(400)
        self.setMaximumHeight(400)
        self.setMaximumWidth(500)

        l = QGridLayout()
        l.addWidget(graph, 0, 1, 10, 10)
        self.setLayout(l)

class ChartDataPoints(QScrollArea):
    def __init__(self, aggregate, dataPoints, isDream=False, teamMembers=[]):
        super().__init__()

        self.aggregate = aggregate
        self.dataPoints = dataPoints
        self.isDream = isDream
        self.teamMembers = teamMembers
        self.tooLittleDataDisclaimer = False

        self.renderCharts()

    def renderCharts(self):
        chartScrollLayout = QVBoxLayout()

        if self.isDream:
            dpLayout = QVBoxLayout()
            title = QLabel("TEAM MEMBERS")
            title.setStyleSheet("font-size:14px;")
            value = QLabel(", ".join(self.teamMembers))
            value.setStyleSheet("font-size:24px;font-weight:bold;")
            dpLayout.addWidget(title)
            dpLayout.addWidget(value)
            dpLayout.setContentsMargins(10, 10, 10, 25)
            chartScrollLayout.addLayout(dpLayout)

        # Chart Widgets
        for k in self.dataPoints:
            i = self.dataPoints[k]
            
            if i[1] == True: # Should be rendered

                # SINGLE DATA POINT
                titleString = k.upper().replace("_", " ")
                if i[2] == "single" or i[2] == "percentile":
                    dpLayout = QVBoxLayout()

                    valueString = str(round(self.aggregate[k], 1))

                    if i[2] == "percentile":
                        titleString += " | BETTER THAN %"

                    title = QLabel(titleString)
                    title.setStyleSheet("font-size:14px;")
                    value = QLabel(valueString)
                    value.setStyleSheet("font-size:24px;font-weight:bold;")

                    dpLayout.addWidget(title)
                    dpLayout.addWidget(value)

                    dpLayout.setContentsMargins(10, 10, 10, 10)

                    chartScrollLayout.addLayout(dpLayout)

                # SPLIT SEASONS GRAPH -> Convert split season data into a list to render on line
                graphData = []

                if i[2] == "split_seasons" or i[2] == "percentile_split_seasons":
                    value = self.aggregate[k]

                    for m in sorted(order.keys()):
                        l = order[m]
                        if l in value:
                            graphData.append((split_seasons_convert_to[m], value[l]))

                    if len(value) > 1:
                        self.tooLittleDataDisclaimer = True
                        continue


                elif i[2] == "line":
                    for n in range(1, len(self.aggregate[k]) + 1):
                        graphData.append((n, self.aggregate[k][n - 1]))

                if i[2] == "split_seasons" or i[2] == "percentile_split_seasons" or i[2] == "line":
                    # GRAPH
                    dpLayout = QVBoxLayout()
                    title = QLabel(titleString)
                    title.setStyleSheet("font-size:14px;")
                    dpLayout.addWidget(title)

                    x, y = [], []
                    for h in graphData:
                        x.append(h[0])
                        y.append(h[1])
                        
                    graph = W(x, y)
                    dpLayout.addWidget(graph, 1000)
                    dpLayout.setContentsMargins(10, 10, 10, 10)
                    chartScrollLayout.addLayout(dpLayout)

                if i[2] == "bar":
                    dpLayout = QVBoxLayout()
                    title = QLabel(titleString)
                    title.setStyleSheet("font-size:14px;")
                    dpLayout.addWidget(title)

                    x, y = [], []
                    for o in self.aggregate[k]:
                        x.append(o[:3])
                        y.append(self.aggregate[k][o])
                        
                    graph = W(x, y, True)

                    dpLayout.addWidget(graph, 1000)
                    dpLayout.setContentsMargins(10, 10, 10, 10)
                    chartScrollLayout.addLayout(dpLayout)

        if self.tooLittleDataDisclaimer:
            a = QLabel("Too little data to split seasons. Graphs not displayed.")
            a.setStyleSheet("color: gray; font: bold 18px;")
            a.setContentsMargins(10, 10, 10, 14)
            chartScrollLayout.addWidget(a)

        chartInner = QWidget()
        chartInner.setLayout(chartScrollLayout)

        self.setWidgetResizable(True)
        self.setWidget(chartInner)
