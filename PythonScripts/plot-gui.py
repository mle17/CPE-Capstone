import sys
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QAction, QLineEdit, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
#******************************************************************
import matplotlib
matplotlib.use("Qt5Agg")
#******************************************************************
from PyQt5 import QtCore
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import random
import DAQ
#******************************************************************

# osc_daq = DAQ.init_osc()
overall_df = pd.DataFrame()

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        # Panel setup option
        self.left = 100
        self.top = 100
        self.title = 'Secure Our System'
        self.width = 1440
        self.height = 960
        self.is_trigger = True

        self.m = self.initUI()

    # params 
    def _initButton(self,button,tooltip,x,y,sizex,sizey):
        button.setToolTip(tooltip)
        button.move(x,y)
        button.resize(sizex,sizey)
    


    def initUI(self):
        # actualy set the panel
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # the graph
        m = PlotCanvas(self, width=5, height=4)
        m.move(10,10)

        # start button
        self.button_start = QPushButton('Start', self)
        self._initButton(self.button_start,'Start Recording',550,70,120,50)
        self.button_start.clicked.connect(self.on_click)

        # Create save button
        self.button_save = QPushButton('Export data', self)
        self._initButton(self.button_save,'Save data as CSV file',550,120,120,50)
        self.button_save.clicked.connect(self.on_export)

        # Create toggle Button 
        self.button_toggle = QPushButton('Trigger/Auto', self)
        self._initButton(self.button_toggle,'Toggle Trigger Mode On and OFF',550,170,120,50)
        self.button_toggle.clicked.connect(self.on_switch_mode)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(670, 130)
        self.textbox.resize(140, 20)
        self.textbox.setPlaceholderText('Enter file name here')
        self.textbox.setText('default');
        self.label_ext = QLabel(".csv", self);
        self.label_ext.move(820,125)

        self.input_times = QLineEdit(self)
        self.input_times.move(670, 70)
        self.input_times.resize(140, 20)
        self.input_times.setPlaceholderText('X TIMES')
        self.input_times.setText('1');

        self.show()
        return m

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        for i in range (int(self.input_times.text())):
            print('is Trigger' + str(self.is_trigger))
            global overall_df
            # wave_data = DAQ.take_waveform(osc_daq, self.is_trigger)
            placeholder_data = pd.DataFrame([random.random() for i in range(25)])
            overall_df = overall_df.append(placeholder_data)

            self.m.setData(placeholder_data.iloc[:,0])
            self.on_export()


    @pyqtSlot()
    def on_export(self):
        print(overall_df)
        overall_df.to_csv(self.textbox.text() + '.csv')

    @pyqtSlot()
    def on_switch_mode(self):
        self.is_trigger = not self.is_trigger
        print(self.is_trigger)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot([random.random() for i in range(25)])


    def plot(self, data):
        print('data' + str(data))
        self.figure.clear()
        ax = self.figure.add_subplot(1,1,1)
        ax.set_title('Waveform')
        self.lines = ax.plot(data, 'r-')
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Voltage (V)')
        self.draw()

    def setData(self, data):
        self.lines.pop(0).remove()
        self.plot(data)

if __name__ == '__main__':
    main()
