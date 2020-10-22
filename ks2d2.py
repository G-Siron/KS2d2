from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QDialog, QWidget, QVBoxLayout, QLabel, QTableWidgetItem, QTableView, QAbstractItemView
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QDoubleValidator
import matplotlib  
matplotlib.use('Qt5Agg')   
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import sys
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from ndtest import ks2d2s
import KS_2s_2d_Layout
import Stats_Window

class KS_2s_2d_App(QMainWindow, KS_2s_2d_Layout.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.home()


## Define all connections for the GUI

    def home(self):
        self.actionQuit.triggered.connect(self.close_application)
        self.pushButton_file.clicked.connect(self.file_browse)
        self.pushButton_run.clicked.connect(self.plot_data)
        self.actionData.triggered.connect(self.Window_pvalue)
        self.actionSave_figure.triggered.connect(self.Save_Figure)
        self.lineEdit_name_pop1.editingFinished.connect(self.name_pop1_def)
        self.lineEdit_name_pop2.editingFinished.connect(self.name_pop2_def)
        self.lineEdit_x_variable.editingFinished.connect(self.x_name_def)
        self.lineEdit_y_variable.editingFinished.connect(self.y_name_def)

## Define all actions for each interaction with the GUI

    def close_application(self):
        choice = QMessageBox.question(self, 'Quit!?',
                                      "Do you really want to quit the application? Any unsaved changes will be lost.",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def file_browse(self):
        global name
        name, _ = QFileDialog.getOpenFileNames(self, "Select the .asc files to import", "Desktop", filter='*.xlsx')

    def name_pop1_def(self):
        global name_pop1
        name_pop1 = None
        name_pop1_str = self.lineEdit_name_pop1.text()
        name_pop1 = str(name_pop1_str) 

    def name_pop2_def(self):
        global name_pop2
        name_pop2 = None
        name_pop2_str = self.lineEdit_name_pop2.text()
        name_pop2 = str(name_pop2_str)

    def import_data(self):
        global Population_1
        global Population_2
        Population_1 = []
        Population_2 = []
        Population_1 = pd.read_excel(name[0], sheet_name=name_pop1)
        Population_2 = pd.read_excel(name[0], sheet_name=name_pop2)
        self.Input_data_construction()

    def x_name_def(self):
        global x_name
        x_name = None
        x_name_str = self.lineEdit_x_variable.text()
        x_name = str(x_name_str) 

    def y_name_def(self):
        global y_name
        y_name = None
        y_name_str = self.lineEdit_y_variable.text()
        y_name = str(y_name_str)

    def Input_data_construction(self):
        global x1
        global y1 
        global x2
        global y2
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        x1 = Population_1[x_name]
        y1 = Population_1[y_name]
        x2 = Population_2[x_name]
        y2 = Population_2[y_name]


    def plot_data(self):
        self.import_data()
        global result
        result = ks2d2s(x1, y1, x2, y2, extra=True)

        # definitions for the axes
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        spacing = 0.01


        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom + height + spacing, width, 0.2]
        rect_histy = [left + width + spacing, bottom, 0.2, height]

        # start with a square Figure
        self.dpi = 100
        self.fig = plt.Figure((12.0, 9.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        ax = self.fig.add_axes(rect_scatter)
        ax_histx = self.fig.add_axes(rect_histx, sharex=ax)
        ax_histy = self.fig.add_axes(rect_histy, sharey=ax)

        # use the previously defined function
        self.scatter_hist(x1, y1, x2, y2, ax, ax_histx, ax_histy)
        self.canvas.show()


    def scatter_hist(self, x1, y1, x2, y2, ax, ax_histx, ax_histy):
        # no labels
        ax_histx.tick_params(axis="x", labelbottom=False)
        ax_histy.tick_params(axis="y", labelleft=False)

        # the scatter plot:
        ax.scatter(x1, y1, label= name_pop1)
        ax.scatter(x2, y2, label= name_pop2)
        ax.set_xlabel(x_name, fontsize=15)
        ax.set_ylabel(y_name, fontsize=15)

        # now determine nice limits by hand:
        binwidth_x = 0.5 * np.std(x1)
        xmax = max(np.max(np.abs(x1)), np.max(np.abs(x2)))
        xmin = min(np.min(x1), np.min(x2))
        max_x = (int(xmax/binwidth_x) + 1) * binwidth_x
        min_x = (int(xmin/binwidth_x) - 1) * binwidth_x
        bins_x = np.arange(min_x - binwidth_x, max_x + binwidth_x, binwidth_x)

        binwidth_y = 0.5 * np.std(y1)
        ymax = max(np.max(np.abs(y1)), np.max(np.abs(y2)))
        ymin = min(np.min(y1), np.min(y2))
        max_y = (int(ymax/binwidth_y) + 1) * binwidth_y
        min_y = (int(ymin/binwidth_y) - 1) * binwidth_y
        bins_y = np.arange(min_y - binwidth_y, max_y + binwidth_y, binwidth_y)

        ax_histx.hist(x1, bins=bins_x)
        ax_histy.hist(y1, bins=bins_y, orientation='horizontal')
        ax_histx.hist(x2, bins=bins_x)
        ax_histy.hist(y2, bins=bins_y, orientation='horizontal')

        ax.set_xlim([min_x,max_x])
        ax.set_ylim([min_y,max_y])
        ax.legend(loc='upper left', fontsize= 15, bbox_to_anchor=(1.1, 1.2))

    def Save_Figure(self):
        name_Fig = QFileDialog.getSaveFileName(self, 'Save Figure')
        name_save_Fig = name_Fig[0] + '.eps'
        self.fig.savefig(name_save_Fig, dpi=300, format=None)

    def Window_pvalue(self):
        self.Stats_show = Stats_Window_show()
        self.Stats_show.show()

class Stats_Window_show(QWidget, Stats_Window.Ui_Form):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.pushButton_saveStats.clicked.connect(self.save_Stats_file)

        global set_text_Stats
        set_text_Stats = 'p-value = ' + str(result[0])
        self.textEdit_Stats.setText(set_text_Stats)

    def save_Stats_file(self):
        name_Stats_file = QFileDialog.getSaveFileName(self, 'Save Figure')
        name_save_Stats_file = name_Stats_file[0] + '.txt'
        stats_file = open(name_save_Stats_file,'w')
        stats_file.write(set_text_Stats)


def main():
    app = QApplication(sys.argv)
    form = KS_2s_2d_App()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()