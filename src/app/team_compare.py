from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget, QLineEdit, QGridLayout, QWidget, QListWidget, QLabel, QPushButton, QScrollArea, QFrame, QButtonGroup, QVBoxLayout
from src.data.metadata import dbPlayers
from src.aggregate.data_points import teamDataPoints, dataPointsWhere
from src.app.utils import getScreenSize
from src.app.chart import ChartDataPoints
from src.aggregate.team import fetch_and_aggregate_team
from src.data.credentials import defaultDatabase

class TeamCompare(QWidget):
    selectedName = ""
    selectedName2 = ""
    teamDataPoints = dict(teamDataPoints)
    buttonState = {}

    def __init__(self, selectedNames, startDates, endDates):
        super().__init__()

        self.selectedName = selectedNames[0]
        self.aggregate = fetch_and_aggregate_team(self.selectedName, defaultDatabase(), start=startDates[0], end=endDates[0])

        self.selectedName2 = selectedNames[1]
        self.aggregate2 = fetch_and_aggregate_team(self.selectedName2, defaultDatabase(), start=startDates[1], end=endDates[1])

        self.dateRangeText = " (" + startDates[0] + " - " + endDates[0] + ")"
        self.dateRangeText2 = " (" + startDates[1] + " - " + endDates[1] + ")"

        # CONFIG
        self.setWindowTitle(" vs ".join(selectedNames))
        size = getScreenSize()
        self.resize(size[0]*0.8, size[1]*1)

        # Create a central widget and layout
        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        self.gridLayout.setRowStretch(8, 100000)
        # self.gridLayout.setColumnStretch(6, 1.2)

        if self.aggregate != {} and self.aggregate2 != {}:
            self.renderBase()
            self.renderButtons()
            self.renderCharts()
        else:
            self.gridLayout.addWidget(QLabel("No records Found!"), 0, 1)


    def renderBase(self):
        # Create a label to display the text
        label = QLabel("Comparing " + self.selectedName + " and " + self.selectedName2)
        label.setStyleSheet("font: bold 30px;")
        label.setContentsMargins(10, 10, 10, 16)
        self.gridLayout.addWidget(label, 1, 0)

        label1 = QLabel(self.selectedName + self.dateRangeText)
        label1.setStyleSheet("font: bold 16px;")
        label1.setContentsMargins(10, 10, 10, 16)
        self.gridLayout.addWidget(label1, 7, 0)

        label2 = QLabel(self.selectedName2 + self.dateRangeText2)
        label2.setStyleSheet("font: bold 16px;")
        label2.setContentsMargins(10, 10, 10, 16)
        self.gridLayout.addWidget(label2, 7, 5)

    def destroyButtons(self):
        self.cat_buttons_layout.deleteLater()
        self.battingScroll.deleteLater()
        self.bowlingScroll.deleteLater()
        self.commonScroll.deleteLater()

    def onAllClick(self):
        for i in self.teamDataPoints:
            self.teamDataPoints[i][1] = not self.buttonState["all"]
        for i in self.buttonState:
            if i == "all":
                continue
            self.buttonState[i] = not self.buttonState["all"]
        
        self.buttonState["all"] = not self.buttonState["all"]

        self.destroyButtons()
        self.renderButtons()
        self.destroyCharts()
        self.renderCharts()

    # Create buttons
    def renderButtons(self):
        # CATEGORIES
        self.cat_buttons_layout = QHBoxLayout()
        self.buttonState["all"] = True
        all_button = self.generateDatapointButton("All", self.onAllClick, self.buttonState["all"])
        self.cat_buttons_layout.addWidget(all_button)
        batting_button = self.generateDatapointButton("Batting", self.generateDatapointLambda("batting", 0, "batting", True), self.buttonState["batting"])
        self.cat_buttons_layout.addWidget(batting_button)
        bowling_button = self.generateDatapointButton("Bowling", self.generateDatapointLambda("bowling", 0, "bowling", True), self.buttonState["bowling"])
        self.cat_buttons_layout.addWidget(bowling_button)
        common_button = self.generateDatapointButton("Common", self.generateDatapointLambda("common", 0, "common", True), self.buttonState["common"])
        self.cat_buttons_layout.addWidget(common_button)
        self.gridLayout.addLayout(self.cat_buttons_layout, 3, 0, 1, 10)

        # BATTING
        self.batting_buttons_layout = QHBoxLayout()
        for i in dataPointsWhere(self.teamDataPoints, 0, "batting"):
            if self.teamDataPoints[i][3] != i:
                continue
            btn = self.generateDatapointButton(i, self.generateDatapointLambda(i, 3, i, True), self.teamDataPoints[i][1])
            self.batting_buttons_layout.addWidget(btn)
        self.battingInner = QWidget()
        self.battingInner.setLayout(self.batting_buttons_layout)
        self.battingScroll = QScrollArea()
        self.battingScroll.setWidgetResizable(True)
        self.battingScroll.setWidget(self.battingInner)
        self.gridLayout.addWidget(self.battingScroll, 4, 0, 1, 10)

        # BOWLING
        self.bowling_buttons_layout = QHBoxLayout()
        for i in dataPointsWhere(self.teamDataPoints, 0, "bowling"):
            if self.teamDataPoints[i][3] != i:
                continue
            btn = self.generateDatapointButton(i, self.generateDatapointLambda(i, 3, i, True), self.teamDataPoints[i][1])
            self.bowling_buttons_layout.addWidget(btn)
        self.bowling_inner = QWidget()
        self.bowling_inner.setLayout(self.bowling_buttons_layout)
        self.bowlingScroll = QScrollArea()
        self.bowlingScroll.setWidgetResizable(True)
        self.bowlingScroll.setWidget(self.bowling_inner)
        self.gridLayout.addWidget(self.bowlingScroll, 5, 0, 1, 10)

        # COMMON
        self.common_buttons_layout = QHBoxLayout()
        for i in dataPointsWhere(self.teamDataPoints, 0, "common"):
            if self.teamDataPoints[i][3] != i:
                continue
            btn = self.generateDatapointButton(i, self.generateDatapointLambda(i, 3, i, True), self.teamDataPoints[i][1])
            self.common_buttons_layout.addWidget(btn)
        self.common_inner = QWidget()
        self.common_inner.setLayout(self.common_buttons_layout)
        self.commonScroll = QScrollArea()
        self.commonScroll.setWidgetResizable(True)
        self.commonScroll.setWidget(self.common_inner)
        self.gridLayout.addWidget(self.commonScroll, 6, 0, 1, 10)

    def destroyCharts(self):
        self.chart.deleteLater()

    def renderCharts(self):
        self.chart = ChartDataPoints(self.aggregate, self.teamDataPoints)
        self.gridLayout.addWidget(self.chart, 8, 0, 10, 5)

        self.chart2 = ChartDataPoints(self.aggregate2, self.teamDataPoints)
        self.gridLayout.addWidget(self.chart2, 8, 5, 10, 6)


    def generateDatapointButton(self, text, onClick, enabled):
        ss = "font: regular 20px; padding: 8px;"
        if not enabled:
            ss += "background-color: #111111; color: white;"
        else:
            ss += "background-color: #266346; color: white;"

        def btnOnClick():
            onClick()

        btn = QPushButton(text=text.replace("_", " ").title())
        btn.clicked.connect(btnOnClick)
        btn.setStyleSheet(ss)
        
        return btn

    def generateDatapointLambda(self, id, index, isValue, toggleStatus, changeStatusTo=True):
        if toggleStatus:
            if id not in self.buttonState:
                self.buttonState[id] = True

        def lm():
            self.buttonState[id] = not self.buttonState[id]
            for i in dataPointsWhere(self.teamDataPoints, index, isValue):
                if toggleStatus:
                    self.teamDataPoints[i][1] = self.buttonState[id]
                else:
                    self.teamDataPoints[i][1] = changeStatusTo

            self.destroyButtons()
            self.renderButtons()
            self.destroyCharts()
            self.renderCharts()

        return lm
    