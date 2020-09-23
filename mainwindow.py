# This Python file uses the following encoding: utf-8

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

from datasources import BPMData
from dataprocessor import DataProcessor
from settingscontrol import SettingsControl


class MainWindow(QMainWindow):
    """   """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('MainWindow.ui', self)

        self.setWindowTitle("Frequency Measurer")
        self.window_str = "None"
        self.frq_founded = 0.0

        self.buttonExit.clicked.connect(self.on_exit_button)
        self.buttonExit.clicked.connect(QApplication.instance().quit)

        self.data_source = BPMData(1024, self)
        self.data_source.data_ready.connect(self.on_data1_ready)
        self.data_source.data_ready.connect(self.on_data3_ready)

        self.data_proc_X = DataProcessor("X")
        self.data_proc_Z = DataProcessor("Z")
        self.data_source.data_ready.connect(self.data_proc_X.on_data_recv)
        self.data_source.data_ready.connect(self.data_proc_Z.on_data_recv)
        self.data_proc_X.data_processed.connect(self.on_data2_ready)
        self.data_proc_Z.data_processed.connect(self.on_data4_ready)

        self.controlWidgetX.window_changed_str.connect(self.data_proc_X.on_wind_changed)
        self.controlWidgetX.groupBox.setTitle("Data_X")
        self.controlWidgetX.set_str_id("Data_X")
        self.controlWidgetX.scale_changed_obj.connect(self.on_scale_changing)

        self.controlWidgetZ.window_changed_str.connect(self.data_proc_Z.on_wind_changed)
        self.controlWidgetZ.groupBox.setTitle("Data_Z")
        self.controlWidgetZ.set_str_id("Data_Z")
        self.controlWidgetZ.scale_changed_obj.connect(self.on_scale_changing)

        self.controlWidgetX.method_changed_str.connect(self.data_proc_X.on_method_changed)
        self.controlWidgetX.boards_changed.connect(self.data_proc_X.on_boards_changed)

        self.controlWidgetZ.method_changed_str.connect(self.data_proc_Z.on_method_changed)
        self.controlWidgetZ.boards_changed.connect(self.data_proc_Z.on_boards_changed)

        self.settingsControl = SettingsControl()
        self.settingsControl.add_object(self.controlWidgetX)
        self.settingsControl.add_object(self.controlWidgetZ)
        self.buttonRead.clicked.connect(self.on_read_button)
        self.buttonSave.clicked.connect(self.on_save_button)
        self.settingsControl.read_settings()

        self.data_proc_X.data_processed.connect(self.on_freq_status_X)
        self.data_proc_Z.data_processed.connect(self.on_freq_status_Z)

        self.plots_customization()
        self.data_curve1 = self.ui.plotX.plot(pen = 'r', title = 'Generated signal X_plot')
        self.data_curve2 = self.ui.plotFX.plot(pen = 'r', title = 'Fourier Transform X_plot')
        self.data_curve3 = self.ui.plotZ.plot(pen = 'b', title='Generated signal Z_plot')
        self.data_curve4 = self.ui.plotFZ.plot(pen = 'b', title='Fourier Transform Z_plot')

    def plots_customization(self):
        """   """

        label_str_x = "<span style=\"color:red;font-size:16px\">{}</span>"
        label_str_z = "<span style=\"color:blue;font-size:16px\">{}</span>"

        self.ui.plotX.setLabel('left', label_str_x.format("X"))
        self.customize_plot(self.ui.plotX)
        self.ui.plotX.setYRange(-4, 4)

        self.ui.plotFX.setLabel('left',label_str_x.format("Ax"))
        self.ui.plotFX.setYRange(0, 0.8, padding =0)
        self.customize_plot(self.ui.plotFX)

        self.ui.plotZ.setLabel('left', label_str_z.format("Z"))
        self.ui.plotZ.setYRange(-2, 2)
        self.customize_plot(self.ui.plotZ)

        self.ui.plotFZ.setLabel('left', label_str_z.format("Az"))
        self.ui.plotFZ.setYRange(0, 0.4)
        self.customize_plot(self.ui.plotFZ)

    def customize_plot(self, plot):
        """   """
        plot.setBackground('w')
        plot.showAxis('top')
        plot.showAxis('right')
        plot.getAxis('top').setStyle(showValues = False)
        plot.getAxis('right').setStyle(showValues=False)
        plot.showGrid(x=True, y=True)

    def on_scale_changing(self, control_widget):
        """   """
        scale = control_widget.scale
        if control_widget.str_id == "Data_X":
            self.plot_mode(self.ui.plotFX, scale)
        elif control_widget.str_id == "Data_Z":
            self.plot_mode(self.ui.plotFZ, scale)
        else:
            print("Error in control_widget!")

    def plot_mode(self, plot, scale):
        """   """
        if scale == "Normal":
            plot.setLogMode(False, False)
        if scale == 'Log_Y':
            plot.setLogMode(False, True)

    # def on_plot_scale_changing(self, plot):
    #     """   """
    #     if self.str_id == "Data X":
    #         print("Sanechek")
    #         self.ui.plotFX.setLogMode(False, True)
    #         pass
    #     elif self.str_id == "Data Z":
    #         pass
    #     else:
    #         pass

    def on_exit_button(self):
        print(self, ' Exiting... Bye...')

    def on_read_button(self):
        self.settingsControl.read_settings()

    def on_save_button(self):
        self.settingsControl.save_settings()

    def on_data1_ready(self, data_source):
        """"   """
        self.data_curve1.setData(data_source.dataT, data_source.dataX)

    def on_data3_ready(self, data_source):
        """   """
        self.data_curve3.setData(data_source.dataT, data_source.dataZ)

    def on_data2_ready(self, data_processor):
        """   """
        self.data_curve2.setData(data_processor.fftwT, data_processor.fftw_to_process)

    def on_data4_ready(self, data_processor):
        """   """
        self.data_curve4.setData(data_processor.fftwT, data_processor.fftw_to_process)

    def on_freq_status_X(self, data_processor):
        if data_processor.warning == 0:
            self.ui.freq_statX.setText('Frequency = {}'.format(data_processor.frq_founded))
        elif data_processor.warning == 1:
            self.ui.freq_statX.setText(data_processor.warningText)
        else:
            self.ui.freq_statX.setText('Warning number has unexpected value!')

        freq_textX = '{:7.6f}'.format(data_processor.frq_founded)
        self.ui.freq_showX.display(freq_textX)

    def on_freq_status_Z(self, data_processor):
        if data_processor.warning == 0:
            self.ui.freq_statZ.setText('Frequency = {}'.format(data_processor.frq_founded))
        elif data_processor.warning == 1:
            self.ui.freq_statZ.setText(data_processor.warningText)
        else:
            self.ui.freq_statZ.setText('Warning number has unexpected value!')

        freq_textZ = '{:7.6f}'.format(data_processor.frq_founded)
        self.ui.freq_showZ.display(freq_textZ)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
