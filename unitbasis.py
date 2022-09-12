from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QWidget, QGridLayout, QLineEdit, QSpacerItem, QSizePolicy, \
    QHBoxLayout, QVBoxLayout, QFormLayout, QApplication
from PyQt5.QtGui import QIcon, QDoubleValidator, QClipboard


class UnitBasis(QWidget):

    def __init__(self):
        super(UnitBasis, self).__init__()
        self.mainLayout = QHBoxLayout()
        self.formLayout = QFormLayout()
        self.formulaLayout = QVBoxLayout()
        self.copyLayout = QVBoxLayout()

        # create our double validator
        doubleValidator = QDoubleValidator()

        # setup the formLayout
        # Unit Price
        self.unitPriceLineEdit = QLineEdit()
        self.unitPriceLineEdit.setValidator(doubleValidator)
        self.formLayout.addRow("Unit Price", self.unitPriceLineEdit)
        # Basis Value
        self.basisValueLineEdit = QLineEdit()
        self.basisValueLineEdit.setValidator(doubleValidator)
        self.formLayout.addRow("Basis Value", self.basisValueLineEdit)
        # Decimal Places
        self.decimalsComboBox = QComboBox()
        self.decimalsComboBox.addItems(('Auto', '0', '1', '2', '3', '4', '5', '6'))
        self.formLayout.addRow("Decimals", self.decimalsComboBox)
        self.formLayout.setSpacing(11)

        # setup the formulaLayout
        self.multiplierValue = QLineEdit()
        self.discountValue = QLineEdit()
        self.markupValue = QLineEdit()
        self.grossProfitValue = QLineEdit()
        self.formulaLayout.addWidget(self.multiplierValue)
        self.formulaLayout.addWidget(self.discountValue)
        self.formulaLayout.addWidget(self.markupValue)
        self.formulaLayout.addWidget(self.grossProfitValue)
        self.formulaLayout.addStretch(1)
        self.formulaLayout.setSpacing(11)

        # setup the copyLoyout
        self.multiplierCopyButton = QPushButton()
        self.multiplierCopyButton.setIcon(QIcon("copy.png"))
        self.discountCopyButton = QPushButton()
        self.discountCopyButton.setIcon(QIcon("copy.png"))
        self.markupCopyButton = QPushButton()
        self.markupCopyButton.setIcon(QIcon("copy.png"))
        self.grossProfitCopyButton = QPushButton()
        self.grossProfitCopyButton.setIcon(QIcon("copy.png"))
        self.copyLayout.addWidget(self.multiplierCopyButton)
        self.copyLayout.addWidget(self.discountCopyButton)
        self.copyLayout.addWidget(self.markupCopyButton)
        self.copyLayout.addWidget(self.grossProfitCopyButton)
        self.copyLayout.addStretch(1)

        # make our connections
        self.unitPriceLineEdit.textChanged.connect(self.calculateFormulas)
        self.basisValueLineEdit.textChanged.connect(self.calculateFormulas)
        self.decimalsComboBox.currentTextChanged.connect(self.calculateFormulas)
        self.multiplierCopyButton.clicked.connect(self.copyMultiplierText)
        self.discountCopyButton.clicked.connect(self.copyDiscountText)
        self.markupCopyButton.clicked.connect(self.copyMarkupText)
        self.grossProfitCopyButton.clicked.connect(self.copyGrossProfitText)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addLayout(self.formulaLayout)
        self.mainLayout.addLayout(self.copyLayout)

        self.setLayout(self.mainLayout)

    def copyMultiplierText(self):
        text = self.multiplierValue.text()
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)

    def copyDiscountText(self):
        text = self.discountValue.text()
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)

    def copyMarkupText(self):
        text = self.markupValue.text()
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)

    def copyGrossProfitText(self):
        text = self.grossProfitValue.text()
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)

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
                self.grossProfitValue.setText(
                    f'GP{round((1.0 - 1 / multiplier) * 100.0, int(self.decimalsComboBox.currentText()))}')
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
            pass
        return -1

    def clearFormulas(self):
        self.multiplierValue.setText('')
        self.discountValue.setText('')
        self.markupValue.setText('')
        self.grossProfitValue.setText('')
