from PyQt5 import QtWidgets


class TicketSpecials(QtWidgets.QWidget):
    def __init__(self, val):
        super().__init__()
        formLayout = QtWidgets.QFormLayout()
        groupBox = QtWidgets.QGroupBox("This Is Group Box")
        labelLis = []
        comboList = []
        for i in range(val):
            labelLis.append(QtWidgets.QLabel("Label"))
            comboList.append(QtWidgets.QPushButton("Click Me"))
            formLayout.addRow(labelLis[i], comboList[i])
        groupBox.setLayout(formLayout)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(scroll)
