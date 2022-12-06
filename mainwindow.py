from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QFileDialog

from unitformula import UnitFormula
from ticketspecials import TicketSpecials
from unitbasis import UnitBasis
from formulaconverter import FormulaConverter


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Pricing Tool")
        self.setWindowIcon(QIcon('sc.ico'))

        self.statusBar()
        self.unitFormulaTab = UnitFormula(parent=self)
        self.unitBasisTab = UnitBasis()
        self.ticketSpecialsTab = TicketSpecials(30)

        self.centralWidget = QTabWidget()

        self._createMenu()
        self._setupCentralWidget()

        self.show()
        self.resizeWindow()
        self.currentFrame = None

    def resizeWindow(self):
        self.resize(self.sizeHint())

    def _createMenu(self):
        # add the exit button
        exitAction = QAction("E&xit", self)
        exitAction.setShortcut("Alt+F4")
        exitAction.setStatusTip('Exit The App')
        exitAction.triggered.connect(self.closeApplication)

        # add the open action for loading the ticket tsv file
        openAction = QAction("&Open", self)
        openAction.setStatusTip("Open an exported ticket")
        openAction.triggered.connect(self.getTicketData)

        # add the save action for saving generated mass load file
        saveAction = QAction("&Save", self)
        saveAction.setStatusTip("Save the generated mass load file")
        saveAction.triggered.connect(self.saveMassLoad)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

    def getTicketData(self):
        fileName = self.openFileNameDialog()
        if fileName:
            print(fileName)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open Ticket To Process",
            "",
            "Tab Separated Files (*.tsv);;All Files (*)",
            options=options
        )
        if fileName:
            return fileName

    def saveMassLoad(self):
        pass

    def _setupCentralWidget(self):
        self.centralWidget.addTab(self.unitFormulaTab, 'Unit Price/Formula')
        self.centralWidget.addTab(self.unitBasisTab, 'Unit Price/Basis')
        self.centralWidget.addTab(self.ticketSpecialsTab, 'Ticket Specials')
        self.setCentralWidget(self.centralWidget)

    def closeApplication(self):
        self.close()

    def loadUnitBasis(self):
        if self.currentFrame:
            self.currentFrame.forget()


    def loadUnitFormula(self):
        pass

    def loadFormulaConverter(self):
        pass

    def loadTicketSpecials(self):
        pass
