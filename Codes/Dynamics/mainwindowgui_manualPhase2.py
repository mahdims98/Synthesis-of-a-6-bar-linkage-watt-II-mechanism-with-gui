from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindowguiPhase2 import *
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.colors as plt_colors
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
import numpy as np

class UiMainWindowManual(Ui_MainWindow):
    def setup_ui(self):
        self.setupUi(self)

        self.color_code = dict()

        self.brushes = dict()
        self.pens = dict()
        self.lineEdit_length = dict()
        self.lineEdit_angle = dict()
        self.lineEdit_omega = dict()
        self.lineEdit_alpha = dict()

        self.dynamic_canvas = dict()
        self.figure = dict()
        self.dynamic_ax = dict()
        self.toolbar = dict()

        self.dynamic_canvas_p = dict()
        self.figure_p = dict()
        self.dynamic_ax_p = dict()
        self.toolbar_p = dict()

        self.dynamic_canvas_z = dict()
        self.figure_z = dict()
        self.dynamic_ax_z = dict()
        self.toolbar_z = dict()


        self.color_code[-1] = "#eb34a2"
        self.color_code[0] = "#4cd137"
        self.color_code[1] = "#fbc531"
        self.color_code[2] = "#e84118"
        self.color_code[3] = "#9c88ff"
        self.color_code[4] = "#60a3bc"




        self.add_line_edits()

    # --------------------------------------
    # --------------------------------------
    def add_line_edits(self):
        for i in range(0, 8):
            self.lineEdit_length[i] = QtWidgets.QLineEdit(self.groupBox_inputs)
            self.lineEdit_length[i].setObjectName("lineEdit")
            self.lineEdit_length[i].setAlignment(QtCore.Qt.AlignCenter)
            self.lineEdit_length[i].setMinimumSize(QtCore.QSize(0, 25))
            if i < 5:
                self.gridLayout.addWidget(self.lineEdit_length[i], i + 1, 1, 1, 1)
            else:
                self.gridLayout.addWidget(self.lineEdit_length[i], i + 2, 1, 1, 1)
        # ---------------------------------------
        # add doublespinbox for length
        # ---------------------------------------
        for i in range(0, 8):
            self.lineEdit_angle[i] = QtWidgets.QLineEdit(self.groupBox_inputs)
            self.lineEdit_angle[i].setObjectName("lineEdit")
            self.lineEdit_angle[i].setAlignment(QtCore.Qt.AlignCenter)
            self.lineEdit_angle[i].setMinimumSize(QtCore.QSize(0, 25))
            if i < 5:
                self.gridLayout.addWidget(self.lineEdit_angle[i], i + 1, 2, 1, 1)
            else:
                self.gridLayout.addWidget(self.lineEdit_angle[i], i + 2, 2, 1, 1)
        # ---------------------------------------
        # add doublespinbox for angular velocity
        # ---------------------------------------
        for i in range(0, 8):
            self.lineEdit_omega[i] = QtWidgets.QLineEdit(self.groupBox_inputs)
            self.lineEdit_omega[i].setObjectName("lineEdit")
            self.lineEdit_omega[i].setReadOnly(True)
            self.lineEdit_omega[i].setText("0")
            self.lineEdit_omega[i].setAlignment(QtCore.Qt.AlignCenter)
            self.lineEdit_omega[i].setMinimumSize(QtCore.QSize(0, 25))
            if i < 5:
                self.gridLayout.addWidget(self.lineEdit_omega[i], i + 1, 3, 1, 1)
            else:
                self.gridLayout.addWidget(self.lineEdit_omega[i], i + 2, 3, 1, 1)
        for i in range(0, 8):
            self.lineEdit_alpha[i] = QtWidgets.QLineEdit(self.groupBox_inputs)
            self.lineEdit_alpha[i].setObjectName("lineEdit")
            self.lineEdit_alpha[i].setText("0")
            self.lineEdit_alpha[i].setReadOnly(True)
            self.lineEdit_alpha[i].setAlignment(QtCore.Qt.AlignCenter)
            self.lineEdit_alpha[i].setMinimumSize(QtCore.QSize(0, 25))
            if i < 5:
                self.gridLayout.addWidget(self.lineEdit_alpha[i], i + 1, 4, 1, 1)
            else:
                self.gridLayout.addWidget(self.lineEdit_alpha[i], i + 2, 4, 1, 1)








