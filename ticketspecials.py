from PyQt5 import QtGui, QtWidgets


class TicketSpecials(QtWidgets.QWidget):
    def __init__(self, val):
        super().__init__()
        self.title = "PyQt5 Scroll Bar"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
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
