# This Python file uses the following encoding: utf-8
#

from PyQt5.QtCore import QCoreApplication, QSettings
import signal
import pyqtgraph as pg
from mainwindow import *

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


# Allow CTRL+C and/or SIGTERM to kill us (PyQt blocks it otherwise)
signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGTERM, signal.SIG_DFL)

if __name__ == "__main__":
    import sys

    QCoreApplication.setOrganizationName("Denisov")
    QCoreApplication.setApplicationName("Freq_Online")
    QSettings.setDefaultFormat(QSettings.IniFormat)

    app = QApplication(sys.argv)

    mw = MainWindow()

    mw.show()
    sys.exit(app.exec_())
