import sys

from PyQt5 import QtWidgets

from mainwindow import MainWindow


def run():
    app = QtWidgets.QApplication(sys.argv)
    _ = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
