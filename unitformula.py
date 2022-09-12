from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QDoubleValidator, QRegularExpressionValidator
from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QFormLayout


class UnitFormula(QWidget):

    def __init__(self, parent=None):
        super(UnitFormula, self).__init__(parent)

        regex = QRegularExpression(r"(?:\*|X|D|\-|\+|GP)-?([0-9]*[.])?[0-9]+",
                                          QRegularExpression.CaseInsensitiveOption)

        doubleValidator = QDoubleValidator()

        self.unitPriceLineEdit = QLineEdit()
        self.unitPriceLineEdit.setValidator(doubleValidator)
        self.formulaLineEdit = QLineEdit()
        formulaValidator = QRegularExpressionValidator(regex, self.formulaLineEdit)
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
        if multiplier <= 0:  # or not self.unitPriceLineEdit.text():
            self.basisLineEdit.setText('')
            return
        if self.decimalsComboBox.currentText() == 'Auto':
            self.basisLineEdit.setText(str(float(self.unitPriceLineEdit.text()) / multiplier))
        elif self.decimalsComboBox.currentText() == '0':
            self.basisLineEdit.setText(str(int(float(self.unitPriceLineEdit.text()) / multiplier)))
        else:
            self.basisLineEdit.setText(
                str(round(float(self.unitPriceLineEdit.text()) / multiplier, int(self.decimalsComboBox.currentText()))))

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
