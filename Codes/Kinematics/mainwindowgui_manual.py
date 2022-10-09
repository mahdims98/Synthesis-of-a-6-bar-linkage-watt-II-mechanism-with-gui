from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindowgui import *
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



        # animation widgets
        self.figure_animation = plt.figure()
        self.figure_animation.patch.set_facecolor("None")
        self.dynamic_canvas_animation = FigureCanvas(self.figure_animation)
        self.dynamic_canvas_animation.setStyleSheet("background-color:#073f5b;")
        self.horizontalLayout_2.addWidget(self.dynamic_canvas_animation)
        self.dynamic_ax_animation = self.dynamic_canvas_animation.figure.subplots()
        self.dynamic_ax_animation.axis('equal')
        self.dynamic_ax_animation.axis('off')




        # -----------------------------------------------------
        # graphs properties


        self.gridLayout_graphs = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_overall)
        self.gridLayout_graphs.setObjectName("gridLayout_graphs ")

        self.gridLayout_graphs_p = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_point_p)
        self.gridLayout_graphs_p.setObjectName("gridLayout_graphs ")

        self.gridLayout_graphs_z = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_point_z)
        self.gridLayout_graphs_z.setObjectName("gridLayout_graphs ")


        plt.rcParams.update({'text.color': "#e1e2e3",
                             'axes.labelcolor': "#e1e2e3",
                             'ytick.color': "#e1e2e3",
                             'xtick.color': "#e1e2e3",
                             'axes.facecolor': "#073f5b", 'figure.max_open_warning': 0})

        # --------------------------------------
        # --------------------------------------
        self.add_line_edits()
        self.add_graphs()
        self.add_graphs_p()
        self.add_graphs_z()

    # --------------------------------------
    # --------------------------------------

    def add_graphs(self):
        for i in range(0, 6):
            self.figure[i] = plt.figure()
            self.figure[i].patch.set_facecolor("None")
            self.dynamic_canvas[i] = FigureCanvas(self.figure[i])
            self.toolbar[i] = NavigationToolbar(self.dynamic_canvas[i], self)
            self.dynamic_canvas[i].setMinimumSize(QtCore.QSize(600, 400))
            # self.dynamic_canvas_theta.setMaximumSize(QtCore.QSize(500, 300))
            self.dynamic_canvas[i].setStyleSheet("background-color:#073f5b;")

            self.gridLayout_graphs.addWidget(self.toolbar[i], 1, i,
                                             QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.gridLayout_graphs.addWidget(self.dynamic_canvas[i], 0, i,
                                             QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.dynamic_ax[i] = self.dynamic_canvas[i].figure.subplots()
            # self.dynamic_canvas_theta.hide()
            # self.toolbar_theta.hide()
            self.dynamic_ax[i].yaxis.grid(True, linestyle='--')
            self.dynamic_ax[i].xaxis.grid(True, linestyle='--')
            self.set_graphs_labels(i)

    def add_graphs_p(self):
        for i in range(0, 9):
            self.figure_p[i] = plt.figure()
            self.figure_p[i].patch.set_facecolor("None")
            self.dynamic_canvas_p[i] = FigureCanvas(self.figure_p[i])
            self.toolbar_p[i] = NavigationToolbar(self.dynamic_canvas_p[i], self)
            self.dynamic_canvas_p[i].setMinimumSize(QtCore.QSize(600, 400))
            # self.dynamic_canvas_theta.setMaximumSize(QtCore.QSize(500, 300))
            self.dynamic_canvas_p[i].setStyleSheet("background-color:#073f5b;")

            self.gridLayout_graphs_p.addWidget(self.toolbar_p[i], 1, i,
                                             QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.gridLayout_graphs_p.addWidget(self.dynamic_canvas_p[i], 0, i,
                                             QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.dynamic_ax_p[i] = self.dynamic_canvas_p[i].figure.subplots()
            # self.dynamic_canvas_theta.hide()
            # self.toolbar_theta.hide()
            self.dynamic_ax_p[i].yaxis.grid(True, linestyle='--')
            self.dynamic_ax_p[i].xaxis.grid(True, linestyle='--')
            self.set_graphs_labels_p(i)

    def add_graphs_z(self):
        for i in range(0, 9):
            self.figure_z[i] = plt.figure()
            self.figure_z[i].patch.set_facecolor("None")
            self.dynamic_canvas_z[i] = FigureCanvas(self.figure_z[i])
            self.toolbar_z[i] = NavigationToolbar(self.dynamic_canvas_z[i], self)

            self.dynamic_canvas_z[i].setMinimumSize(QtCore.QSize(600, 400))
            # self.dynamic_canvas_theta.setMaximumSize(QtCore.QSize(500, 300))
            self.dynamic_canvas_z[i].setStyleSheet("background-color:#073f5b;")

            self.gridLayout_graphs_z.addWidget(self.toolbar_z[i], 1, i,
                                             QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.gridLayout_graphs_z.addWidget(self.dynamic_canvas_z[i], 0, i,
                                             QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.dynamic_ax_z[i] = self.dynamic_canvas_z[i].figure.subplots()
            # self.dynamic_canvas_theta.hide()
            # self.toolbar_theta.hide()
            self.dynamic_ax_z[i].yaxis.grid(True, linestyle='--')
            self.dynamic_ax_z[i].xaxis.grid(True, linestyle='--')
            self.set_graphs_labels_z(i)


    # --------------------------------------
    # --------------------------------------


    def set_graphs_labels(self, i):
        self.dynamic_ax[i].yaxis.grid(True, linestyle='--')
        self.dynamic_ax[i].xaxis.grid(True, linestyle='--')
        if i == 0:
            self.dynamic_ax[i].set_title('θ')
            self.dynamic_ax[i].set_ylabel('θ (°)')
            self.dynamic_ax[i].set_xlabel('θ2 (°)')
        elif i == 1:
            self.dynamic_ax[i].set_title('ω')
            self.dynamic_ax[i].set_ylabel('ω (rads)')
            self.dynamic_ax[i].set_xlabel('θ2 (°)')
        elif i == 2:
            self.dynamic_ax[i].set_title('α ')
            self.dynamic_ax[i].set_ylabel('α (rad/s²)')
            self.dynamic_ax[i].set_xlabel('θ2 (°)')
        elif i == 3:
            self.dynamic_ax[i].set_title("θ' ")
            self.dynamic_ax[i].set_ylabel("θ' (rad/rad)")
            self.dynamic_ax[i].set_xlabel('θ2 (°)')
        elif i == 4:
            self.dynamic_ax[i].set_title('θ" ')
            self.dynamic_ax[i].set_ylabel('θ" (rad²/rad²)')
            self.dynamic_ax[i].set_xlabel('θ2 (°)')
        elif i == 5:
            self.dynamic_ax[i].set_title("det of θ'")
            self.dynamic_ax[i].set_ylabel("det of θ'")
            self.dynamic_ax[i].set_xlabel('θ2 (°)')

    # **********************************
    # **********************************


    def set_graphs_labels_p(self, i):
        self.dynamic_ax_p[i].yaxis.grid(True, linestyle='--')
        self.dynamic_ax_p[i].xaxis.grid(True, linestyle='--')
        if i == 0:
            self.dynamic_ax_p[i].set_title('P coordinates')
            self.dynamic_ax_p[i].set_ylabel('coordinates (m)')
            self.dynamic_ax_p[i].set_xlabel('θ2 (°)')
        elif i == 1:
            self.dynamic_ax_p[i].set_title('P velocity')
            self.dynamic_ax_p[i].set_ylabel('velocity (m/s²)')
            self.dynamic_ax_p[i].set_xlabel('θ2 (°)')
        elif i == 2:
            self.dynamic_ax_p[i].set_title('P acceleration ')
            self.dynamic_ax_p[i].set_ylabel('acceleration (m/s)')
            self.dynamic_ax_p[i].set_xlabel('θ2 (°)')
        elif i == 3:
            self.dynamic_ax_p[i].set_title("P first kinematic coefficient ")
            self.dynamic_ax_p[i].set_ylabel("X' & Y' (m/m)")
            self.dynamic_ax_p[i].set_xlabel('θ2 (°)')
        elif i == 4:
            self.dynamic_ax_p[i].set_title('P second kinematic coefficient ')
            self.dynamic_ax_p[i].set_ylabel('X" & Y" (m²/m²)')
            self.dynamic_ax_p[i].set_xlabel('θ2 (°)')
        elif i == 5:
            self.dynamic_ax_p[i].set_title('P center of curvature coordinate ')
            self.dynamic_ax_p[i].set_ylabel('coordinates (m)')
            self.dynamic_ax_p[i].set_xlabel('θ2 (°)')
            self.dynamic_ax_p[i].set_ylim([-75, +75])

        elif i == 6:
            self.dynamic_ax_p[i].set_title('P radius of curvature ')
            self.dynamic_ax_p[i].set_ylabel('radius of curvature (m)')
            self.dynamic_ax_p[i].set_xlabel('θ2 (°)')
            self.dynamic_ax_p[i].set_ylim([-75, +75])

        elif i == 7:
            self.dynamic_ax_p[i].set_title('P Tangential vector')
            self.dynamic_ax_p[i].set_ylabel('Tx & Ty (m)')
            self.dynamic_ax_p[i].set_xlabel('θ2 (°)')
        elif i == 8:
            self.dynamic_ax_p[i].set_title('P Normal vector')
            self.dynamic_ax_p[i].set_ylabel('Nx & Ny (m)')
            self.dynamic_ax_p[i].set_xlabel('θ2 (°)')

    # --------------------------------------
    # --------------------------------------
    def set_graphs_labels_z(self, i):
        self.dynamic_ax_z[i].yaxis.grid(True, linestyle='--')
        self.dynamic_ax_z[i].xaxis.grid(True, linestyle='--')
        if i == 0:
            self.dynamic_ax_z[i].set_title('Z coordinates')
            self.dynamic_ax_z[i].set_ylabel('coordinates (m)')
            self.dynamic_ax_z[i].set_xlabel('θ2 (°)')
        elif i == 1:
            self.dynamic_ax_z[i].set_title('Z velocity')
            self.dynamic_ax_z[i].set_ylabel('velocity (m/s²)')
            self.dynamic_ax_z[i].set_xlabel('θ2 (°)')
        elif i == 2:
            self.dynamic_ax_z[i].set_title('Z acceleration ')
            self.dynamic_ax_z[i].set_ylabel('acceleration (m/s)')
            self.dynamic_ax_z[i].set_xlabel('θ2 (°)')
        elif i == 3:
            self.dynamic_ax_z[i].set_title("Z first kinematic coefficient ")
            self.dynamic_ax_z[i].set_ylabel("X' & Y' (m/m)")
            self.dynamic_ax_z[i].set_xlabel('θ2 (°)')
        elif i == 4:
            self.dynamic_ax_z[i].set_title('Z second kinematic coefficient ')
            self.dynamic_ax_z[i].set_ylabel('X" & Y" (m²/m²)')
            self.dynamic_ax_z[i].set_xlabel('θ2 (°)')
        elif i == 5:
            self.dynamic_ax_z[i].set_title('Z center of curvature coordinate ')
            self.dynamic_ax_z[i].set_ylabel('coordinates (m)')
            self.dynamic_ax_z[i].set_xlabel('θ2 (°)')
            self.dynamic_ax_z[i].set_ylim([-75, +75])
        elif i == 6:
            self.dynamic_ax_z[i].set_title('Z radius of curvature ')
            self.dynamic_ax_z[i].set_ylabel('radius of curvature (m)')
            self.dynamic_ax_z[i].set_xlabel('θ2 (°)')
            self.dynamic_ax_z[i].set_ylim([-75, +75])
        elif i == 7:
            self.dynamic_ax_z[i].set_title('Z Tangential vector')
            self.dynamic_ax_z[i].set_ylabel('Tx & Ty (m)')
            self.dynamic_ax_z[i].set_xlabel('θ2 (°)')
        elif i == 8:
            self.dynamic_ax_z[i].set_title('Z Normal vector')
            self.dynamic_ax_z[i].set_ylabel('Nx & Ny (m)')
            self.dynamic_ax_z[i].set_xlabel('θ2 (°)')

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








