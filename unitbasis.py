from PyQt5 import QtGui, QtWidgets


class UnitBasis(QtWidgets.QWidget):

    def __init__(self):
        super(UnitBasis, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.formLayout = QtWidgets.QFormLayout()

        # create our double validator
        doubleValidator = QtGui.QDoubleValidator()

        # add widgets to formlayout
        self.unitPriceLineEdit = QtWidgets.QLineEdit()
        self.unitPriceLineEdit.setValidator(doubleValidator)
        self.basisValueLineEdit = QtWidgets.QLineEdit()
        self.basisValueLineEdit.setValidator(doubleValidator)
        self.decimalsComboBox = QtWidgets.QComboBox()
        self.decimalsComboBox.addItems(('Auto', '0', '1', '2', '3', '4', '5', '6'))
        self.formLayout.addRow('Unit Price', self.unitPriceLineEdit)
        self.formLayout.addRow('Basis Value', self.basisValueLineEdit)
        self.formLayout.addRow('Decimals', self.decimalsComboBox)

        # add widgets to the verticalLayout
        self.multiplierValue = QtWidgets.QLineEdit()
        self.discountValue = QtWidgets.QLineEdit()
        self.markupValue = QtWidgets.QLineEdit()
        self.grossProfitValue = QtWidgets.QLineEdit()
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
