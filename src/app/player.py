from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget, QLineEdit, QGridLayout, QWidget, QListWidget, QLabel, QPushButton, QScrollArea, QFrame, QButtonGroup, QVBoxLayout
from src.data.metadata import dbPlayers
from src.aggregate.data_points import dataPoints, dataPointsWhere
from src.app.utils import getScreenSize


class PlayerWindow(QWidget):
    selectedName = ""
    playerDataPoints = dict(dataPoints)
    buttonState = {}

    def __init__(self, selectedNames):
        super().__init__()

        self.selectedName = selectedNames[0]

        # CONFIG
        self.setWindowTitle("Statify")
        size = getScreenSize()
        self.resize(size[0]*0.8, size[1]*0.8)
        self.setMaximumWidth(size[1]*0.8)

        # Create a central widget and layout
        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        self.renderButtons()

    def renderBase(self):
        # Create a label to display the text
        label = QLabel(self.selectedName)
        label.setStyleSheet("font: bold 36px;")
        self.gridLayout.addWidget(label)

    def destroyButtons(self):
        self.cat_buttons_layout.deleteLater()
        self.battingScroll.deleteLater()
        self.bowlingScroll.deleteLater()
        self.commonScroll.deleteLater()

    # Create buttons
    def renderButtons(self):
        print("RENDER BUTTONS")

        # CATEGORIES
        self.cat_buttons_layout = QHBoxLayout()
        self.gridLayout.addLayout(self.cat_buttons_layout, 3, 1)
        batting_button = self.generateDatapointButton("Batting", self.generateDatapointLambda("batting", 0, "batting", True), self.buttonState["batting"])
        self.cat_buttons_layout.addWidget(batting_button)
        bowling_button = self.generateDatapointButton("Bowling", self.generateDatapointLambda("bowling", 0, "bowling", True), self.buttonState["bowling"])
        self.cat_buttons_layout.addWidget(bowling_button)
        common_button = self.generateDatapointButton("Common", self.generateDatapointLambda("common", 0, "common", True), self.buttonState["common"])
        self.cat_buttons_layout.addWidget(common_button)

        # BATTING
        self.batting_buttons_layout = QHBoxLayout()
        for i in dataPointsWhere(self.playerDataPoints, 0, "batting"):
            if self.playerDataPoints[i][3] != i:
                continue
            btn = self.generateDatapointButton(i, self.generateDatapointLambda(i, 3, i, True), self.playerDataPoints[i][1])
            self.batting_buttons_layout.addWidget(btn)
        self.battingInner = QWidget()
        self.battingInner.setLayout(self.batting_buttons_layout)
        self.battingScroll = QScrollArea()
        self.battingScroll.setWidgetResizable(True)
        self.battingScroll.setWidget(self.battingInner)
        self.gridLayout.addWidget(self.battingScroll, 4, 1)

        # BOWLING
        self.bowling_buttons_layout = QHBoxLayout()
        for i in dataPointsWhere(self.playerDataPoints, 0, "bowling"):
            if self.playerDataPoints[i][3] != i:
                continue
            btn = self.generateDatapointButton(i, self.generateDatapointLambda(i, 3, i, True), self.playerDataPoints[i][1])
            self.bowling_buttons_layout.addWidget(btn)
        self.bowling_inner = QWidget()
        self.bowling_inner.setLayout(self.bowling_buttons_layout)
        self.bowlingScroll = QScrollArea()
        self.bowlingScroll.setWidgetResizable(True)
        self.bowlingScroll.setWidget(self.bowling_inner)
        self.gridLayout.addWidget(self.bowlingScroll, 5, 1)

        # COMMON
        self.common_buttons_layout = QHBoxLayout()
        for i in dataPointsWhere(self.playerDataPoints, 0, "common"):
            if self.playerDataPoints[i][3] != i:
                continue
            btn = self.generateDatapointButton(i, self.generateDatapointLambda(i, 3, i, True), self.playerDataPoints[i][1])
            self.common_buttons_layout.addWidget(btn)
        self.common_inner = QWidget()
        self.common_inner.setLayout(self.common_buttons_layout)
        self.commonScroll = QScrollArea()
        self.commonScroll.setWidgetResizable(True)
        self.commonScroll.setWidget(self.common_inner)
        self.gridLayout.addWidget(self.commonScroll, 6, 1)

    def destroyCharts(self):
        self.chartScroll.deleteLater()

    def renderCharts(self):
        chartScrollLayout = QVBoxLayout()

        # Chart Widgets
        chartScrollLayout.addWidget(QWidget())

        chartInner = QWidget()
        chartInner.setLayout(chartScrollLayout)

        self.chartScroll = QScrollArea()
        self.chartScroll.setWidgetResizable(True)
        self.chartScroll.setWidget(chartInner)
        
        self.gridLayout.addWidget(self.chartScroll, 7, 1, 10, 8)


    def generateDatapointButton(self, text, onClick, enabled):
        ss = "font: regular 20px;"
        if not enabled:
            ss += "background-color: #111111; color: white;"
        else:
            ss += "background-color: #266346; color: white;"

        def btnOnClick():
            onClick()

        btn = QPushButton(text=text)
        btn.clicked.connect(btnOnClick)
        btn.setStyleSheet(ss)
        
        return btn

    def generateDatapointLambda(self, id, index, isValue, toggleStatus, changeStatusTo=True):
        if toggleStatus:
            if id not in self.buttonState:
                self.buttonState[id] = True

        def lm():
            self.buttonState[id] = not self.buttonState[id]
            for i in dataPointsWhere(self.playerDataPoints, index, isValue):
                if toggleStatus:
                    self.playerDataPoints[i][1] = self.buttonState[id]
                else:
                    self.playerDataPoints[i][1] = changeStatusTo

            self.renderButtons()

        return lm
    
    def buttonClicked(self):
        sender = self.sender()  # Get the button that was clicked
        button_name = sender.text()  # Get the text of the button
        print(f'{button_name}')
        self.close()  # Close the window
