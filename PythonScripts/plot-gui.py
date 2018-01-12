import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QAction, QLineEdit, QWidget, QPushButton
from PyQt5.QtGui import QIcon
#******************************************************************
import matplotlib
matplotlib.use("Qt5Agg")
#******************************************************************
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import random
import DAQ
#******************************************************************

osc_daq = DAQ.init_osc()
overall_df = pd.DataFrame()

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        # Panel
        self.left = 100
        self.top = 100
        self.title = 'Secure Our System'
        self.width = 1440
        self.height = 960
        self.is_trigger = True
        self.m = self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # the graph
        m = PlotCanvas(self, width=10, height=8)
        m.move(0,0)

        button = QPushButton('Start', self)
        button.setToolTip('Start Data Recording')
        button.move(580,0)
        button.resize(140,100)
        button.clicked.connect(self.on_click)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(520, 120)
        self.textbox.resize(140, 20)
        self.textbox.setPlaceholderText('Enter file name here')

        # Create a button in the window
        self.button_save = QPushButton('Save data', self)
        self.button_save.setToolTip('Sava data as txt file')
        self.button_save.move(520,170)
        button.resize(140,100)

        # connect button to function on_click
        self.button_save.clicked.connect(self.on_save)

        self.show()
        return m

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        # put data here
        wave_data = DAQ.take_waveform(osc_daq, self.is_trigger)
        global overall_df
        overall_df = overall_df.append(wave_data)
        self.m.setData(list(wave_data.iloc[0]))

    @pyqtSlot()
    def on_save(self):
        print(overall_df)
        overall_df.to_csv(self.textbox.text())

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # self.data = [random.random() for i in range(25)]
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot([random.random() for i in range(25)])


    def plot(self, data):

        # data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
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
