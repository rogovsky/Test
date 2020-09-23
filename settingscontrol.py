# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 17:48:20 2020

@author: Вячеслав
"""
from PyQt5.QtCore import pyqtSignal, Qt, QObject


class SettingsControl(QObject):
    """   """
    save_data = pyqtSignal(object)
    read_data = pyqtSignal(QObject)

    def __init__(self, parent = None):
        super(SettingsControl, self).__init__(parent)

        self.obj_list = []

    def add_object(self, object):
        self.obj_list.append(object)

    def save_settings(self):
        """   """
        for obj in self.obj_list:
            obj.save_settings()

    def read_settings(self):
        """   """
        for obj in self.obj_list:
            obj.read_settings()
