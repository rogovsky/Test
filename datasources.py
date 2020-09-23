#
#
#

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout

import numpy as np


class BPMData(QObject):
    """   """
    data_ready = pyqtSignal(object)

    def __init__(self, bpm_name='', parent=None):
        super(BPMData, self).__init__(parent)

        self.bpm_name = bpm_name
        self.num_pts = 1024
        self.data_len = self.num_pts

        self.dataT = None
        self.dataX = None
        self.dataZ = None
        self.dataI = None

        self.def_time = 1000
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_update)
        self.timer.start(self.def_time)

    def on_timer_update(self):
        """   """
        self.generate_bpm_data()
        self.data_ready.emit(self)

    def generate_bpm_data(self):
        """   """
        self.dataT = np.arange(0, self.data_len, dtype=float)
        self.dataX = np.sin(2 * np.pi * 0.25 * self.dataT) + 2 * np.cos(2 * np.pi * 0.4 * self.dataT) # Frq = 0.25 + Frq = 0.4
        self.dataZ = np.exp(-1 * 0.15 * 10.0e-8 * self.dataT * self.dataT) * np.cos(2 * np.pi * 0.1 * self.dataT) # Frq = 0.1, dec = 0.15
        self.dataI = np.ones(self.data_len)
        self.dataX = self.dataX + 0.3 * np.random.normal(size=self.data_len) # 30% noise
        self.dataZ = self.dataZ + 0.1 * np.random.normal(size=self.data_len) # 10% noise
