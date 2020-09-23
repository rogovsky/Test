#
#
#

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt, QObject

import numpy as np

import pycx4.qcda as cda


class BPMData(QObject):
    """   """
    data_ready = pyqtSignal(object)

    def __init__(self, bpm_name = '', parent=None):
        super(BPMData, self).__init__(parent)

        self.bpm_name = bpm_name
        self.num_pts = 1024
        self.data_len = self.num_pts

        self.tmp = None
        self.dataT = None
        self.dataX = None
        self.dataZ = None
        self.dataI = None

        self.lboard = 0.01
        self.rboard = 0.5

        self.bpmChan        = cda.VChan('v2cx::hemera:4.5@s', max_nelems = 8 * 1024 * 4, dtype = cda.CXDTYPE_INT32)
        self.bpmChan_numpts = cda.IChan('v2cx::hemera:4.5@p10')

        self.bpmChan_numpts.valueMeasured.connect(self._on_numpts_update)
        self.bpmChan.valueMeasured.connect(self._on_signal_update)

    def _on_signal_update(self, chan):
        # print('Signal received ... = {}'.format(chan.val))
        print('Signal received ...')
        self.tmp = np.frombuffer(chan.val.data, dtype = np.dtype('f4'))

    def _on_numpts_update(self, chan):
        print('Numpts received ... = {}'.format(chan.val))
        self.num_pts = chan.val
        self.data_len = self.num_pts
        
        self.tmp = np.reshape(self.tmp, (4, self.num_pts))

        self.dataT = self.tmp[0]
        self.dataX = self.tmp[1]
        self.dataZ = self.tmp[2]
        self.dataI = self.tmp[3]

        self.data_ready.emit(self)
       
        
