from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction

from unitformula import UnitFormula
from ticketspecials import TicketSpecials
from unitbasis import UnitBasis


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Pricing Tool")
        self.setWindowIcon(QIcon('sc.ico'))

        self.statusBar()
        self.unitPriceFormulaTab = UnitFormula(parent=self)
        self.unitBasisTab = UnitBasis()
        self.ticketSpecialsTab = TicketSpecials(30)

        self.centralWidget = QTabWidget()

        self._createMenu()
        self._setupCentralWidget()

        self.show()
        self.resizeWindow()

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
        pass

    def saveMassLoad(self):
        pass

    def _setupCentralWidget(self):
        self.centralWidget.addTab(self.unitPriceFormulaTab, 'Unit Price/Formula')
        self.centralWidget.addTab(self.unitBasisTab, 'Unit Price/Basis')
        self.centralWidget.addTab(self.ticketSpecialsTab, 'Ticket Specials')
        self.setCentralWidget(self.centralWidget)

    def closeApplication(self):
        self.close()
