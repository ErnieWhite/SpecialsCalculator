import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import (
    QIcon,
    QDoubleValidator,
    QRegExpValidator,
)
from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    QApplication,
    QWidget,
    QFormLayout,
    QTabWidget,
    QGridLayout,
    QLineEdit,
    QComboBox,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
    QGroupBox,
    QPushButton,
    QFileDialog,
)


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Pricing Tool")
        self.setWindowIcon(QIcon('pythonlogo.png'))
        self._createMenu()

        self.statusBar()

        self.centralWidget = QTabWidget()

        self.home()
        self.resizeWindow()

    def resizeWindow(self):
        self.resize(self.sizeHint())

    def _createMenu(self):
        extractAction = QAction("&Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

    def home(self):
        self.unitPriceFormulaTab = UnitFormula()
        self.unitBasisTab = UnitBasis()
        self.ticketSpecialsTab = TicketSpecials(30)
        self.centralWidget.addTab(self.unitPriceFormulaTab, 'Unit Price/Formula')
        self.centralWidget.addTab(self.unitBasisTab, 'Unit Price/Basis')
        self.centralWidget.addTab(self.ticketSpecialsTab, 'Ticket Specials')

        self.setCentralWidget(self.centralWidget)
        self.show()

    def close_application(self):
        self.close()


class TicketSpecials(QWidget):
    def __init__(self, val):
        super().__init__()
        self.title = "PyQt5 Scroll Bar"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        formLayout = QFormLayout()
        groupBox = QGroupBox("This Is Group Box")
        labelLis = []
        comboList = []
        for i in range(val):
            labelLis.append(QLabel("Label"))
            comboList.append(QPushButton("Click Me"))
            formLayout.addRow(labelLis[i], comboList[i])
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(400)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


class UnitBasis(QWidget):
    def __init__(self):
        super(UnitBasis, self).__init__()
        self.horizontalLayout = QHBoxLayout()
        self.verticalLayout = QVBoxLayout()
        self.formLayout = QFormLayout()


        # create our double validator
        doubleValidator = QDoubleValidator()

        # add widgets to formlayout
        self.unitPriceLineEdit = QLineEdit()
        self.unitPriceLineEdit.setValidator(doubleValidator)
        self.basisValueLineEdit = QLineEdit()
        self.basisValueLineEdit.setValidator(doubleValidator)
        self.decimalsComboBox = QComboBox()
        self.decimalsComboBox.addItems(('Auto', '0', '1', '2', '3', '4', '5', '6'))
        self.formLayout.addRow('Unit Price', self.unitPriceLineEdit)
        self.formLayout.addRow('Basis Value', self.basisValueLineEdit)
        self.formLayout.addRow('Decimals', self.decimalsComboBox)

        # add widgets to the verticalLayout
        self.multiplierValue = QLineEdit()
        self.discountValue = QLineEdit()
        self.markupValue = QLineEdit()
        self.grossProfitValue = QLineEdit()
        self.verticalLayout.addWidget(self.multiplierValue)
        self.verticalLayout.addWidget(self.discountValue)
        self.verticalLayout.addWidget(self.markupValue)
        self.verticalLayout.addWidget(self.grossProfitValue)
        self.verticalLayout.addStretch(2)
        self.horizontalLayout.addLayout(self.formLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)

        # make our connections
        self.unitPriceLineEdit.textChanged.connect(self.calculateFormulas)
        self.basisValueLineEdit.textChanged.connect(self.calculateFormulas)
        self.decimalsComboBox.currentTextChanged.connect(self.calculateFormulas)

        self.setLayout(self.horizontalLayout)

    def calculateFormulas(self):
        if not self.unitPriceLineEdit.text() or not self.basisValueLineEdit.text():
            self.clearFormulas()
            return
        if self.unitPriceLineEdit.text() == '.' or self.basisValueLineEdit.text() == '.':
            self.clearFormulas()
            return
        multiplier = float(self.unitPriceLineEdit.text()) / float(self.basisValueLineEdit.text())
        if self.decimalsComboBox.currentText() == 'Auto':
            self.multiplierValue.setText(f'*{multiplier}')
            self.discountValue.setText(f'{(multiplier - 1) * 100:+}')
            self.markupValue.setText(f'D{1 / multiplier}')
            numeric_part = (1.1 - 1 / multiplier) * 100
            if numeric_part < 100:
                self.grossProfitValue.setText(f'GP{(1.0 - 1 / multiplier) * 100.0}')
            else:
                self.grossProfitValue.setText('')
        elif self.decimalsComboBox.currentText() == '0':
            self.multiplierValue.setText(f'*{int(multiplier)}')
            self.discountValue.setText(f'{int((multiplier - 1) * 100):+}')
            self.markupValue.setText(f'D{int(1 / multiplier)}')
            numeric_part = (1.1 - 1 / multiplier) * 100
            if numeric_part < 100:
                self.grossProfitValue.setText(f'GP{int((1.0 - 1 / multiplier) * 100.0)}')
            else:
                self.grossProfitValue.setText('')
        else:
            self.multiplierValue.setText(f'*{round(multiplier, int(self.decimalsComboBox.currentText()))}')
            self.discountValue.setText(f'{round((multiplier - 1) * 100, int(self.decimalsComboBox.currentText())):+}')
            self.markupValue.setText(f'D{round(1 / multiplier, int(self.decimalsComboBox.currentText()))}')
            numeric_part = (1.1 - 1 / multiplier) * 100
            if numeric_part < 100:
                self.grossProfitValue.setText(f'GP{round((1.0 - 1 / multiplier) * 100.0, int(self.decimalsComboBox.currentText()))}')
            else:
                self.grossProfitValue.setText('')

    @staticmethod
    def findMultiplier(formula: str) -> float:
        """Converts a string formula to a float multiplier

            A return value of -1 indicates error
        """
        try:
            print(formula)
            if formula[0] in '+-':
                return 1 + float(formula) / 100
            if formula[0].upper() == 'D':
                return 1 / float(formula[1:])
            if formula.upper().startswith('GP') and len(formula) > 2:
                return 1 / (1 - float(formula[2:]) / 100)
            if formula[0].upper() in '*X':
                return float(formula[1:])
        except (ZeroDivisionError, ValueError):
            return -1
        return -1

    def clearFormulas(self):
        self.multiplierValue.setText('')
        self.discountValue.setText('')
        self.markupValue.setText('')
        self.grossProfitValue.setText('')


class UnitFormula(QWidget):
    def __init__(self):
        super(UnitFormula, self).__init__()

        regex = QRegExp(r"(?:\*|X|D|\-|\+|GP)-?([0-9]*[.])?[0-9]+")
        regex.setCaseSensitivity(False)

        doubleValidator = QDoubleValidator()

        self.unitPriceLineEdit = QLineEdit()
        self.unitPriceLineEdit.setValidator(doubleValidator)
        self.formulaLineEdit = QLineEdit()
        formulaValidator = QRegExpValidator(regex, self.formulaLineEdit)
        self.formulaLineEdit.setValidator(formulaValidator)
        self.decimalsComboBox = QComboBox()
        self.decimalsComboBox.addItems(('Auto', '0', '1', '2', '3', '4', '5', '6'))
        self.basisLineEdit = QLineEdit()

        layout = QFormLayout()
        layout.addRow('Unit Price', self.unitPriceLineEdit)
        layout.addRow('Formula', self.formulaLineEdit)
        layout.addRow('Decimals', self.decimalsComboBox)
        layout.addRow('Base', self.basisLineEdit)
        self.setLayout(layout)

        self.unitPriceLineEdit.textChanged.connect(self.calculateBasis)
        self.formulaLineEdit.textChanged.connect(self.calculateBasis)
        self.decimalsComboBox.currentTextChanged.connect(self.calculateBasis)

    def calculateBasis(self):
        if not self.unitPriceLineEdit.text() or not self.formulaLineEdit.text():
            self.basisLineEdit.setToolTip('')
            return
        multiplier = self.findMultiplier(self.formulaLineEdit.text())
        if multiplier <= 0: # or not self.unitPriceLineEdit.text():
            self.basisLineEdit.setText('')
            return
        if self.decimalsComboBox.currentText() == 'Auto':
            self.basisLineEdit.setText(str(float(self.unitPriceLineEdit.text()) / multiplier))
        elif self.decimalsComboBox.currentText() == '0':
            self.basisLineEdit.setText(str(int(float(self.unitPriceLineEdit.text()) / multiplier)))
        else:
            self.basisLineEdit.setText(str(round(float(self.unitPriceLineEdit.text()) / multiplier, int(self.decimalsComboBox.currentText()))))

    @staticmethod
    def findMultiplier(formula: str) -> float:
        """Converts a string formula to a float multiplier

            A return value of -1 indicates error
        """
        try:
            print(formula)
            if formula[0] in '+-':
                return 1 + float(formula) / 100
            if formula[0].upper() == 'D':
                return 1 / float(formula[1:])
            if formula.upper().startswith('GP') and len(formula) > 2:
                return 1 / (1 - float(formula[2:]) / 100)
            if formula[0].upper() in '*X':
                return float(formula[1:])
        except (ZeroDivisionError, ValueError):
            return -1
        return -1


def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
