# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 17:53:07 2019

@author: Вячеслав
"""

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import uic


class ControlWidget(QWidget):
    """   """
    window_changed_str = pyqtSignal(str)
    method_changed_str = pyqtSignal(str)
    boards_changed = pyqtSignal(object)
    scale_changed_obj = pyqtSignal(object)

    default_str_id = "Warning"

    def __init__(self, parent = None):
        super(ControlWidget, self).__init__(parent)
        self.ui = uic.loadUi('ControlWidget.ui', self)

        self.window = "None"
        self.method = "None"
        self.boards = None
        self.lboard = 0.01
        self.rboard = 0.5
        self.scale = "None"

        self.str_id = self.default_str_id

        buttons = [
            self.usePeakBtn,
            self.useGassiorBtn,
            self.useNaffBtn,
        ]

        id = 1
        for btn in buttons:
            btn.setStyleSheet("QPushButton {background-color: none}"
                              "QPushButton:checked {background-color: green}")
            self.buttonGroup.setId(btn, id)
            id = id + 1

        self.lboardSBox.setValue(0.05)
        self.rboardSBox.setValue(0.3)

        self.checkWindowBox.currentIndexChanged.connect(self.on_window_checked)
        self.buttonGroup.buttonClicked['int'].connect(self.on_method_checked)
        self.lboardSBox.valueChanged.connect(self.on_lboardsbox_changed)
        self.rboardSBox.valueChanged.connect(self.on_rboardsbox_changed)
        self.scalingBox.currentIndexChanged.connect(self.on_plot_checked)

    def on_window_checked(self, state):
        """   """

        if state == 0:
            self.window = "None"
        elif state == 1:
            self.window = "Hann"
        elif state == 2:
            self.window = "Hamming"
        else:
            self.window = "None"

        self.window_changed_str.emit(self.window)

    def on_method_checked(self, state):
        """   """
        print('method_state = ', state)

        if state == 0:
            self.method = "None"
        elif state == 1:
            self.method = "Peak"
        elif state == 2:
            self.method = "Gassior"
        elif state == 3:
            self.method = "Naff"
        else:
            self.method = "None"

        self.method_changed_str.emit(self.method)

    def on_lboardsbox_changed(self, value):
        """   """
        self.lboard = value
        self.on_boards_changed()

    def on_rboardsbox_changed(self, value):
        """   """
        self.rboard = value
        self.on_boards_changed()

    def on_plot_checked(self, state):
        """   """
        if state == 0:
            self.scale = "Normal"
        elif state == 1:
            self.scale = "Log_Y"
        else:
            self.scale = "Normal"

        self.scale_changed_obj.emit(self)

    def on_boards_changed(self):
        """   """
        self.boards = {
            "lboard": self.lboard,
            "rboard": self.rboard
        }
        self.boards_changed.emit(self.boards)

    def set_str_id(self, str):
        self.str_id = str

    def save_settings(self):
        """   """
        if self.str_id == self.default_str_id:
            print(self.default_str_id)
            return

        settings = QSettings()
        settings.beginGroup(self.str_id)
        settings.setValue("window", self.window)
        settings.setValue("method", self.method)
        settings.setValue("lboard", self.lboard)
        settings.setValue("rboard", self.rboard)
        settings.setValue("scale", self.scale)

        print("Saved!!!!!")

        settings.endGroup()
        settings.sync()

    def read_settings(self):

        if self.str_id == "Data_X":

            settings = QSettings()
            settings.beginGroup(self.str_id)
            self.window = settings.value("window", "None")
            self.method = settings.value("method", "None")
            self.lboard = settings.value("lboard", 0.10, type = float)
            self.rboard = settings.value("rboard", 0.25, type = float)
            self.scale = settings.value("scale", "Normal")
            settings.endGroup()


            print("lboard type = ", type(self.lboard))



        elif self.str_id == "Data_Z":
            settings = QSettings()
            settings.beginGroup(self.str_id)
            self.window = settings.value("window", "Hann")
            self.method = settings.value("method", "Peak")
            self.lboard = settings.value("lboard", 0.10, type = float)
            self.rboard = settings.value("rboard", 0.30, type = float)
            self.scale = settings.value("scale", "Normal")
            settings.endGroup()

        else:
            print("Have no SETTINGS!!!!!")

        self.checkWindowBox.setCurrentText(self.window)
        self.window_changed_str.emit(self.window)

        self.scalingBox.setCurrentText(self.scale)
        self.scale_changed_obj.emit(self)

        self.lboardSBox.setValue(self.lboard)
        self.rboardSBox.setValue(self.rboard)

        if self.method == "Peak":
            self.usePeakBtn.setChecked(True)
        elif self.method == "Gassior":
            self.useGassiorBtn.setChecked(True)
        elif self.method == "Naff":
            self.useNaffBtn.setChecked(True)
        self.method_changed_str.emit(self.method)
















