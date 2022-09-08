from PyQt5 import QtGui, QtWidgets

from unitformula import UnitFormula
from ticketspecials import TicketSpecials
from unitbasis import UnitBasis


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Pricing Tool")
        self.setWindowIcon(QtGui.QIcon('sc.ico'))

        self.statusBar()
        self.unitPriceFormulaTab = UnitFormula(parent=self)
        self.unitBasisTab = UnitBasis()
        self.ticketSpecialsTab = TicketSpecials(30)

        self.centralWidget = QtWidgets.QTabWidget()

        self._createMenu()
        self._setupCentralWidget()

        self.show()
        self.resizeWindow()

    def resizeWindow(self):
        self.resize(self.sizeHint())

    def _createMenu(self):
        extractAction = QtWidgets.QAction("&Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

    def _setupCentralWidget(self):
        self.centralWidget.addTab(self.unitPriceFormulaTab, 'Unit Price/Formula')
        self.centralWidget.addTab(self.unitBasisTab, 'Unit Price/Basis')
        self.centralWidget.addTab(self.ticketSpecialsTab, 'Ticket Specials')
        self.setCentralWidget(self.centralWidget)

    def close_application(self):
        self.close()

