# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './mainwindowgui.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1480, 857)
        MainWindow.setStyleSheet("*{font-family: \"Calibri\";\n"
"font-size:15px;\n"
"}\n"
"\n"
"QCheckBox{color:#fafafa}\n"
"\n"
"QComboBox{background-color:#cfd8dc; border-radius:10px; color: #000000 }\n"
"QComboBox::drop-down \n"
"{\n"
"    border: 0px; /* This seems to replace the whole arrow of the combo box */\n"
"}\n"
"QComboBox::down-arrow {\n"
"\n"
"    width: 14px;\n"
"    height: 14px;\n"
"}\n"
"\n"
"\n"
"\n"
".QMainWindow{background-color:#cfd8dc;}\n"
"\n"
"QGroupBox{background-color:#094869;\n"
"\n"
"border-radius:10px;}\n"
"\n"
"\n"
"\n"
"QSpinBox{background-color:#cfd8dc; border-radius:3px;color:black;}\n"
"QSpinBox::drop-down \n"
"{\n"
"\n"
"    border: 1px; /* This seems to replace the whole arrow of the combo box */\n"
"}\n"
"QSpinBox::down-arrow {\n"
"\n"
"    width: 14px;\n"
"    height: 14px;\n"
"}\n"
"QSpinBox::up-arrow {\n"
"\n"
"    width: 14px;\n"
"    height: 14px;\n"
"\n"
"}\n"
"QSpinBox::disabled{ background-color:#e0e0e0;; border-radius:3px;color: #455A64;}\n"
"\n"
"\n"
"QDoubleSpinBox{background-color:#cfd8dc;; border-radius:3px;color: #000000;}\n"
"QDoubleSpinBox::drop-down \n"
"{\n"
"    border: 1px; /* This seems to replace the whole arrow of the combo box */\n"
"}\n"
"QDoubleSpinBox::down-arrow {\n"
"\n"
"\n"
"    width: 14px;\n"
"    height: 14px;\n"
"}\n"
"QDoubleSpinBox::up-arrow {\n"
"\n"
"    width: 14px;\n"
"    height: 14px;\n"
"\n"
"}\n"
"QDoubleSpinBox::disabled{ background-color:#e0e0e0;; border-radius:3px;color: #455A64;}\n"
"\n"
"QLineEdit{background-color:#cfd8dc; border-radius:3px;color: #000000}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 1437, 1085))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_inputs = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_inputs.setMinimumSize(QtCore.QSize(350, 500))
        self.groupBox_inputs.setMaximumSize(QtCore.QSize(500, 16777215))
        self.groupBox_inputs.setStyleSheet("QLabel{font-family: \"Calibri\";\n"
"font-size:15px;\n"
"color:#fafafa;\n"
"}")
        self.groupBox_inputs.setTitle("")
        self.groupBox_inputs.setObjectName("groupBox_inputs")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_inputs)
        self.gridLayout.setContentsMargins(20, -1, 20, -1)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.label_19 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 12, 3, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 0, 4, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 11, 3, 1, 1)
        self.doubleSpinBox_steps = QtWidgets.QDoubleSpinBox(self.groupBox_inputs)
        self.doubleSpinBox_steps.setMinimumSize(QtCore.QSize(0, 25))
        self.doubleSpinBox_steps.setStyleSheet("")
        self.doubleSpinBox_steps.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_steps.setAccelerated(True)
        self.doubleSpinBox_steps.setMaximum(100000.0)
        self.doubleSpinBox_steps.setSingleStep(0.01)
        self.doubleSpinBox_steps.setProperty("value", 0.1)
        self.doubleSpinBox_steps.setObjectName("doubleSpinBox_steps")
        self.gridLayout.addWidget(self.doubleSpinBox_steps, 11, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox_inputs)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 10, 0, 1, 5)
        self.label_6 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.groupBox_inputs)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 6, 0, 1, 5)
        self.spinBox_animation_speed = QtWidgets.QSpinBox(self.groupBox_inputs)
        self.spinBox_animation_speed.setMinimumSize(QtCore.QSize(0, 25))
        self.spinBox_animation_speed.setStyleSheet("")
        self.spinBox_animation_speed.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_animation_speed.setMinimum(1)
        self.spinBox_animation_speed.setMaximum(1000)
        self.spinBox_animation_speed.setProperty("value", 20)
        self.spinBox_animation_speed.setObjectName("spinBox_animation_speed")
        self.gridLayout.addWidget(self.spinBox_animation_speed, 12, 4, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 11, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.spinBox_export_step = QtWidgets.QSpinBox(self.groupBox_inputs)
        self.spinBox_export_step.setMinimumSize(QtCore.QSize(0, 25))
        self.spinBox_export_step.setStyleSheet("")
        self.spinBox_export_step.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_export_step.setProperty("value", 5)
        self.spinBox_export_step.setObjectName("spinBox_export_step")
        self.gridLayout.addWidget(self.spinBox_export_step, 12, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_inputs)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 12, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 8, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_inputs)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 9, 0, 1, 1)
        self.spinBox_repeats = QtWidgets.QSpinBox(self.groupBox_inputs)
        self.spinBox_repeats.setMinimumSize(QtCore.QSize(0, 25))
        self.spinBox_repeats.setSizeIncrement(QtCore.QSize(0, 0))
        self.spinBox_repeats.setStyleSheet("")
        self.spinBox_repeats.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_repeats.setAccelerated(True)
        self.spinBox_repeats.setMaximum(10000000)
        self.spinBox_repeats.setProperty("value", 3600)
        self.spinBox_repeats.setObjectName("spinBox_repeats")
        self.gridLayout.addWidget(self.spinBox_repeats, 11, 4, 1, 1)
        self.pushButton_start = QtWidgets.QPushButton(self.groupBox_inputs)
        self.pushButton_start.setMinimumSize(QtCore.QSize(90, 40))
        self.pushButton_start.setStyleSheet("\n"
".QPushButton{background-color:#094869;\n"
"color: #fafafa;\n"
" border:4px solid #1e88e5; border-radius: 20px;}\n"
".QPushButton:hover{background-color:#1e88e5;}\n"
".QPushButton:disabled{background-color:#757575; border:4px solid #757575;}\n"
"")
        self.pushButton_start.setObjectName("pushButton_start")
        self.gridLayout.addWidget(self.pushButton_start, 13, 2, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_inputs)
        self.groupBox_animation = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_animation.setMinimumSize(QtCore.QSize(700, 500))
        self.groupBox_animation.setStyleSheet("*{font-family: \"Calibri\";\n"
"font-size:15px;\n"
"color:#fafafa;\n"
"}")
        self.groupBox_animation.setTitle("")
        self.groupBox_animation.setObjectName("groupBox_animation")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_animation)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout.addWidget(self.groupBox_animation)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.scrollAreaWidgetContents_3)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.tab)
        self.scrollArea_2.setMinimumSize(QtCore.QSize(0, 500))
        self.scrollArea_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_overall = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_overall.setGeometry(QtCore.QRect(0, 0, 1387, 501))
        self.scrollAreaWidgetContents_overall.setObjectName("scrollAreaWidgetContents_overall")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_overall)
        self.horizontalLayout_9.addWidget(self.scrollArea_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.scrollArea_point_p = QtWidgets.QScrollArea(self.tab_3)
        self.scrollArea_point_p.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_point_p.setWidgetResizable(True)
        self.scrollArea_point_p.setObjectName("scrollArea_point_p")
        self.scrollAreaWidgetContents_point_p = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_point_p.setGeometry(QtCore.QRect(0, 0, 1387, 501))
        self.scrollAreaWidgetContents_point_p.setObjectName("scrollAreaWidgetContents_point_p")
        self.scrollArea_point_p.setWidget(self.scrollAreaWidgetContents_point_p)
        self.horizontalLayout_10.addWidget(self.scrollArea_point_p)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.scrollArea_point_z = QtWidgets.QScrollArea(self.tab_4)
        self.scrollArea_point_z.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_point_z.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scrollArea_point_z.setWidgetResizable(True)
        self.scrollArea_point_z.setObjectName("scrollArea_point_z")
        self.scrollAreaWidgetContents_point_z = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_point_z.setGeometry(QtCore.QRect(0, 0, 1387, 501))
        self.scrollAreaWidgetContents_point_z.setObjectName("scrollAreaWidgetContents_point_z")
        self.scrollArea_point_z.setWidget(self.scrollAreaWidgetContents_point_z)
        self.horizontalLayout_11.addWidget(self.scrollArea_point_z)
        self.tabWidget.addTab(self.tab_4, "")
        self.verticalLayout_6.addWidget(self.tabWidget)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout.addWidget(self.scrollArea_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1480, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_19.setText(_translate("MainWindow", "Anim.  Speed:"))
        self.label_12.setText(_translate("MainWindow", "Alpha"))
        self.label_14.setText(_translate("MainWindow", "Repeats:"))
        self.label_4.setText(_translate("MainWindow", "Vector 3"))
        self.label_6.setText(_translate("MainWindow", "Vector 5"))
        self.label_13.setText(_translate("MainWindow", "Steps:"))
        self.label_2.setText(_translate("MainWindow", "Length"))
        self.label_11.setText(_translate("MainWindow", "Omega"))
        self.label_8.setText(_translate("MainWindow", "Vector 4\'"))
        self.label_3.setText(_translate("MainWindow", "Angle"))
        self.label_5.setText(_translate("MainWindow", "Vector 4"))
        self.label.setText(_translate("MainWindow", "Vector 2"))
        self.label_15.setText(_translate("MainWindow", "Export step"))
        self.label_7.setText(_translate("MainWindow", "Vector 6"))
        self.label_9.setText(_translate("MainWindow", "Vector 1"))
        self.label_10.setText(_translate("MainWindow", "Vector 1\'"))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Overall"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Point P"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Point Z"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
