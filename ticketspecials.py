from PyQt5 import QtWidgets
import csv


class TicketSpecials(QtWidgets.QWidget):
    def __init__(self, val):
        super().__init__()
        formLayout = QtWidgets.QFormLayout()
        groupBox = QtWidgets.QGroupBox("This Is Group Box")
        labelList = []
        pushButtonList = []
        for i in range(val):
            labelList.append(QtWidgets.QLabel("Label"))
            pushButtonList.append(QtWidgets.QPushButton("Click Me"))
            formLayout.addRow(labelList[i], pushButtonList[i])
        groupBox.setLayout(formLayout)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(scroll)


