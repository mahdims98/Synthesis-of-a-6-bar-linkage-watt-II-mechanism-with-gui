from SolverClass import *
from mainwindowgui import *
from mainwindowgui_manual import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np
import sys
import time
import csv
import os
import shutil


class CentreAlignDelegate(QItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignCenter
        QItemDelegate.paint(self, painter, option, index)


# class ProgressBarDialog(QtWidgets.QDialog):


class MainWindowEXEC(QtWidgets.QMainWindow, UiMainWindowManual):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setup_ui()
        self.set_default_values()

        self.show_step = 5
        self.export_step = 5
        self.link_thickness = 0.005
        self.link_length_scale = 1000

        self.angles = np.zeros(8)
        self.lengths = np.zeros(8)
        self.omegas = np.zeros(8)
        self.alphas = np.zeros(8)
        self.vectors = dict()
        self.patches = [None] * 5

        # ***************************************

        # ***************************************
        self.pushButton_start.clicked.connect(self.start_calculation)

        self.showMaximized()
        sys.exit(app.exec_())

    def set_default_values(self):
        # vector 2
        self.lineEdit_length[0].setText("0.05715")
        self.lineEdit_angle[0].setText("0")

        # vector 3
        self.lineEdit_length[1].setText("0.18415")
        self.lineEdit_angle[1].setText("63.95")

        # vector 4
        self.lineEdit_length[2].setText("0.1778")
        self.lineEdit_angle[2].setText("291.5")

        # vector 5
        self.lineEdit_length[3].setText("0.0508")
        self.lineEdit_angle[3].setText("140")

        # vector 6
        self.lineEdit_length[4].setText("0.127")
        self.lineEdit_angle[4].setText("42.3")

        # vector 4 prime
        self.lineEdit_length[5].setText("0.127")
        self.lineEdit_angle[5].setText("320")

        # vector 1
        self.lineEdit_length[6].setText("0.2032")
        self.lineEdit_angle[6].setText("180")

        # vector 1 prime
        self.lineEdit_length[7].setText("0.1016")
        self.lineEdit_angle[7].setText("180")

    def start_calculation(self):
        """ at first we get vector values from lineEdits. then we make an SixLinkSolver Object with given
            vectors. after that we solve the equations. then we plot calculated data
            note that:
            self.vectors[0] : Vector 2
            self.vectors[1] : Vector 3
            self.vectors[2] : Vector 4
            self.vectors[3] : Vector 5
            self.vectors[4] : Vector 6
            self.vectors[5] : Vector 1
            self.vectors[6] : Vector 1 prime
            self.vectors[7] : Vector 4 prime
            """

        self.dynamic_ax_animation.clear()
        self.patches = [None] * 5

        for i in range(0, 8):
            self.lengths[i] = float(self.lineEdit_length[i].text())
            self.angles[i] = float(self.lineEdit_angle[i].text())
            self.omegas[i] = float(self.lineEdit_omega[i].text())
            self.alphas[i] = float(self.lineEdit_alpha[i].text())

        self.vectors[0] = KnownVector(self.lengths[0], self.angles[0])  # vector 2
        self.vectors[6] = KnownVector(self.lengths[6], self.angles[6])  # vector 1
        self.vectors[7] = KnownVector(self.lengths[7], self.angles[7])  # 1 prime vector
        self.vectors[5] = UnKnownVector(self.lengths[5])  # vector 4 prime

        for i in range(1, 5):
            self.vectors[i] = UnKnownVector(float(self.lengths[i]))
            # vector 3 (i = 1) /// vector 4 (i=2)/// vector 5 (i=3) vector 6 (i=4)

        initial_guess_loop_1 = np.array([float(self.angles[1]), float(self.angles[2])])
        initial_guess_loop_2 = np.array([float(self.angles[3]), float(self.angles[4])])

        self.step = self.doubleSpinBox_steps.value()
        self.repeats = self.spinBox_repeats.value()
        self.animation_speed = self.spinBox_animation_speed.value()
        self.export_step = self.spinBox_export_step.value()

        self.solver = SixLinkSolver(known_vectors=(self.vectors[6], self.vectors[7], self.vectors[0]),
                                    unknown_vectors=(
                                        self.vectors[1], self.vectors[2], self.vectors[5], self.vectors[3],
                                        self.vectors[4]),
                                    initial_guesses=(initial_guess_loop_1, initial_guess_loop_2), steps=self.step,
                                    num_of_repeats=self.repeats)
        self.solver.calculate_angular_properties()

        # *****************************
        # *******Time to graph!********
        # *****************************

        for graph_number in range(0, 6):
            self.dynamic_ax[graph_number].clear()
            self.set_graphs_labels(graph_number)
            if graph_number == 0:
                for vector_index in range(1, 5):
                    self.dynamic_ax[graph_number].plot(self.solver.angle_matrix[:, 0],
                                                       self.solver.angle_matrix[:, vector_index],
                                                       label="θ" + str(vector_index + 2),
                                                       color=self.color_code[vector_index])
                    self.dynamic_ax[graph_number].legend(loc='lower left',
                                                         ncol=1, borderaxespad=0.5)
                    self.dynamic_ax[graph_number].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()

            if graph_number == 1:
                for vector_index in range(1, 5):
                    self.dynamic_ax[graph_number].plot(self.solver.angle_matrix[:, 0],
                                                       self.solver.angular_velocity_matrix[:, vector_index],
                                                       label="ω" + str(vector_index + 2),
                                                       color=self.color_code[vector_index])
                    self.dynamic_ax[graph_number].legend(loc='lower left',
                                                         ncol=1, borderaxespad=0.5)
                    self.dynamic_ax[graph_number].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()

            if graph_number == 2:
                for vector_index in range(1, 5):
                    self.dynamic_ax[graph_number].plot(self.solver.angle_matrix[:, 0],
                                                       self.solver.angular_acceleration_matrix[:, vector_index],
                                                       label="α" + str(vector_index + 2),
                                                       color=self.color_code[vector_index])
                    self.dynamic_ax[graph_number].legend(loc='lower left',
                                                         ncol=1, borderaxespad=0.5)
                    self.dynamic_ax[graph_number].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()

            if graph_number == 3:
                for vector_index in range(1, 5):
                    self.dynamic_ax[graph_number].plot(self.solver.angle_matrix[:, 0],
                                                       self.solver.theta_prime_matrix[:, vector_index],
                                                       label="θ'" + str(vector_index + 2),
                                                       color=self.color_code[vector_index])
                    self.dynamic_ax[graph_number].legend(loc='lower left',
                                                         ncol=1, borderaxespad=0.5)
                    self.dynamic_ax[graph_number].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()
            if graph_number == 4:
                for vector_index in range(1, 5):
                    self.dynamic_ax[graph_number].plot(self.solver.angle_matrix[:, 0],
                                                       self.solver.theta_zegond_matrix[:, vector_index],
                                                       label='θ"' + str(vector_index + 2),
                                                       color=self.color_code[vector_index])
                    self.dynamic_ax[graph_number].legend(loc='lower left',
                                                         ncol=1, borderaxespad=0.5)
                    self.dynamic_ax[graph_number].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()

            if graph_number == 5:
                for loop_index in range(0, 2):
                    self.dynamic_ax[graph_number].plot(self.solver.angle_matrix[:, 0],
                                                       self.solver.matrix_det_of_coefficients[:, loop_index],
                                                       label="det of loop'" + str(loop_index+1),
                                                       color=self.color_code[loop_index])
                    self.dynamic_ax[graph_number].legend(loc='lower left',
                                                         ncol=1, borderaxespad=0.5)
                    self.dynamic_ax[graph_number].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()

            # ***********************************
            # ********** point p ****************
            # ***********************************
        for graph_number_p in range(0, 9):
            self.dynamic_ax_p[graph_number_p].clear()
            self.set_graphs_labels_p(graph_number_p)
            if graph_number_p == 0:
                for coordinate_number in range(0, 2):
                    coordinate_text = ["x coordinate", "y coordinate"]
                    self.dynamic_ax_p[graph_number_p].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.p_coordinates_matrix[:, coordinate_number],
                                                           label=coordinate_text[coordinate_number],
                                                           color=self.color_code[coordinate_number])
                    self.dynamic_ax_p[graph_number_p].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_p[graph_number_p].figure.canvas.draw()

                    QtWidgets.QApplication.processEvents()

            if graph_number_p == 1:
                for velocity_number in range(0, 2):
                    velocity_text = ["Vx ", "Vy "]
                    self.dynamic_ax_p[graph_number_p].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.p_velocity_matrix[:, velocity_number],
                                                           label=velocity_text[velocity_number],
                                                           color=self.color_code[velocity_number])
                    self.dynamic_ax_p[graph_number_p].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_p[graph_number_p].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()

            if graph_number_p == 2:
                for acceleration_number in range(0, 2):
                    acceleration_text = ["ax ", "ay "]
                    self.dynamic_ax_p[graph_number_p].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.p_acceleration_matrix[:, acceleration_number],
                                                           label=acceleration_text[acceleration_number],
                                                           color=self.color_code[acceleration_number])
                    self.dynamic_ax_p[graph_number_p].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_p[graph_number_p].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()

            if graph_number_p == 3:
                for first_kinematic_coefficient_number in range(0, 2):
                    first_kinematic_coefficient_text = ["X' ", "Y' "]
                    self.dynamic_ax_p[graph_number_p].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.p_prime_matrix[:,
                                                           first_kinematic_coefficient_number],
                                                           label=first_kinematic_coefficient_text[
                                                               first_kinematic_coefficient_number],
                                                           color=self.color_code[first_kinematic_coefficient_number])
                    self.dynamic_ax_p[graph_number_p].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_p[graph_number_p].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()
            if graph_number_p == 4:
                for second_kinematic_coefficient_number in range(0, 2):
                    second_kinematic_coefficient_text = ['X" ', 'Y" ']
                    self.dynamic_ax_p[graph_number_p].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.p_zegond_matrix[:,
                                                           second_kinematic_coefficient_number],
                                                           label=second_kinematic_coefficient_text[
                                                               second_kinematic_coefficient_number],
                                                           color=self.color_code[second_kinematic_coefficient_number])
                    self.dynamic_ax_p[graph_number_p].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_p[graph_number_p].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()

            if graph_number_p == 5:
                for center_of_curvature_coordinate_number in range(0, 2):
                    coordinate_text = ["x coordinate", "y coordinate"]
                    self.dynamic_ax_p[graph_number_p].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.p_center_of_curvature_matrix[:,
                                                           center_of_curvature_coordinate_number],
                                                           label=coordinate_text[center_of_curvature_coordinate_number],
                                                           color=self.color_code[center_of_curvature_coordinate_number])
                    self.dynamic_ax_p[graph_number_p].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_p[graph_number_p].figure.canvas.draw()
                QtWidgets.QApplication.processEvents()

            if graph_number_p == 6:
                radius_of_curvature_text = ["radius of curvature"]
                self.dynamic_ax_p[graph_number_p].plot(self.solver.angle_matrix[:, 0],
                                                       self.solver.p_radius_of_curvature_matrix[:,
                                                       0],
                                                       label=radius_of_curvature_text[0],
                                                       color=self.color_code[0])
                self.dynamic_ax_p[graph_number_p].legend(loc='lower left',
                                                         ncol=1, borderaxespad=0.5)
                self.dynamic_ax_p[graph_number_p].figure.canvas.draw()
                QtWidgets.QApplication.processEvents()

            if graph_number_p == 7:
                for vector_num in range(0, 2):
                    vector_text = ["Tangential x coordinate (Tx)", "Tangential y coordinate (Ty)"]
                    self.dynamic_ax_p[graph_number_p].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.p_tangential_vector_matrix[:,
                                                           vector_num],
                                                           label=vector_text[vector_num],
                                                           color=self.color_code[vector_num])
                    self.dynamic_ax_p[graph_number_p].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_p[graph_number_p].figure.canvas.draw()
                QtWidgets.QApplication.processEvents()

            if graph_number_p == 8:
                for vector_num in range(0, 2):
                    vector_text = ["Normal x coordinate (Nx)", "Normal y coordinate (Ny)"]
                    self.dynamic_ax_p[graph_number_p].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.p_normal_vector_matrix[:,
                                                           vector_num],
                                                           label=vector_text[vector_num],
                                                           color=self.color_code[vector_num])
                    self.dynamic_ax_p[graph_number_p].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_p[graph_number_p].figure.canvas.draw()
                QtWidgets.QApplication.processEvents()

            # ***********************************
            # ********** point z ****************
            # ***********************************

        for graph_number_z in range(0, 9):
            self.dynamic_ax_z[graph_number_z].clear()
            self.set_graphs_labels_z(graph_number_z)
            if graph_number_z == 0:
                for coordinate_number in range(0, 2):
                    coordinate_text = ["x coordinate", "y coordinate"]
                    self.dynamic_ax_z[graph_number_z].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.z_coordinates_matrix[:, coordinate_number],
                                                           label=coordinate_text[coordinate_number],
                                                           color=self.color_code[coordinate_number])
                    self.dynamic_ax_z[graph_number_z].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_z[graph_number_z].figure.canvas.draw()

                    QtWidgets.QApplication.processEvents()

            if graph_number_z == 1:
                for velocity_number in range(0, 2):
                    velocity_text = ["Vx ", "Vy "]
                    self.dynamic_ax_z[graph_number_z].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.z_velocity_matrix[:, velocity_number],
                                                           label=velocity_text[velocity_number],
                                                           color=self.color_code[velocity_number])
                    self.dynamic_ax_z[graph_number_z].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_z[graph_number_z].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()

            if graph_number_z == 2:
                for acceleration_number in range(0, 2):
                    acceleration_text = ["ax ", "ay "]
                    self.dynamic_ax_z[graph_number_z].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.z_acceleration_matrix[:, acceleration_number],
                                                           label=acceleration_text[acceleration_number],
                                                           color=self.color_code[acceleration_number])
                    self.dynamic_ax_z[graph_number_z].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_z[graph_number_z].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()

            if graph_number_z == 3:
                for first_kinematic_coefficient_number in range(0, 2):
                    first_kinematic_coefficient_text = ["X' ", "Y' "]
                    self.dynamic_ax_z[graph_number_z].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.z_prime_matrix[:,
                                                           first_kinematic_coefficient_number],
                                                           label=first_kinematic_coefficient_text[
                                                               first_kinematic_coefficient_number],
                                                           color=self.color_code[first_kinematic_coefficient_number])
                    self.dynamic_ax_z[graph_number_z].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_z[graph_number_z].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()
            if graph_number_z == 4:
                for second_kinematic_coefficient_number in range(0, 2):
                    second_kinematic_coefficient_text = ['X" ', 'Y" ']
                    self.dynamic_ax_z[graph_number_z].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.z_zegond_matrix[:,
                                                           second_kinematic_coefficient_number],
                                                           label=second_kinematic_coefficient_text[
                                                               second_kinematic_coefficient_number],
                                                           color=self.color_code[second_kinematic_coefficient_number])
                    self.dynamic_ax_z[graph_number_z].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_z[graph_number_z].figure.canvas.draw()
                    QtWidgets.QApplication.processEvents()

            if graph_number_z == 5:
                for center_of_curvature_coordinate_number in range(0, 2):
                    coordinate_text = ["x coordinate", "y coordinate"]
                    self.dynamic_ax_z[graph_number_z].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.z_center_of_curvature_matrix[:,
                                                           center_of_curvature_coordinate_number],
                                                           label=coordinate_text[center_of_curvature_coordinate_number],
                                                           color=self.color_code[center_of_curvature_coordinate_number])
                    self.dynamic_ax_z[graph_number_z].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_z[graph_number_z].figure.canvas.draw()
                QtWidgets.QApplication.processEvents()

            if graph_number_z == 6:
                radius_of_curvature_text = ["radius of curvature"]
                self.dynamic_ax_z[graph_number_z].plot(self.solver.angle_matrix[:, 0],
                                                       self.solver.z_radius_of_curvature_matrix[:,
                                                       0],
                                                       label=radius_of_curvature_text[0],
                                                       color=self.color_code[0])
                self.dynamic_ax_z[graph_number_z].legend(loc='lower left',
                                                         ncol=1, borderaxespad=0.5)
                self.dynamic_ax_z[graph_number_z].figure.canvas.draw()
                QtWidgets.QApplication.processEvents()

            if graph_number_z == 7:
                for vector_num in range(0, 2):
                    vector_text = ["Tangential x coordinate (Tx)", "Tangential y coordinate (Ty)"]
                    self.dynamic_ax_z[graph_number_z].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.z_tangential_vector_matrix[:,
                                                           vector_num],
                                                           label=vector_text[vector_num],
                                                           color=self.color_code[vector_num])
                    self.dynamic_ax_z[graph_number_z].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_z[graph_number_z].figure.canvas.draw()
                QtWidgets.QApplication.processEvents()

            if graph_number_z == 8:
                for vector_num in range(0, 2):
                    vector_text = ["Normal x coordinate (Nx)", "Normal y coordinate (Ny)"]
                    self.dynamic_ax_z[graph_number_z].plot(self.solver.angle_matrix[:, 0],
                                                           self.solver.z_normal_vector_matrix[:,
                                                           vector_num],
                                                           label=vector_text[vector_num],
                                                           color=self.color_code[vector_num])
                    self.dynamic_ax_z[graph_number_z].legend(loc='lower left',
                                                             ncol=1, borderaxespad=0.5)
                    self.dynamic_ax_z[graph_number_z].figure.canvas.draw()
                QtWidgets.QApplication.processEvents()

        #   **********************************
        #   EXCEL Time
        #   **********************************
        self.export_excel()

        #   **********************************
        #   animation loop
        #   **********************************
        start_step = 0

        for i in range(0, self.repeats - 1, self.show_step):
            end_step = i
            start_drawing_time = time.time()
            self.draw_links(i)
            time_spent = 0
            for j in np.arange(start_step, end_step + 1):
                if np.abs(self.solver.angular_velocity_matrix[j, 0]) > 0.000001:
                    time_spent += np.abs(self.solver.angle_matrix[j + 1, 0] - self.solver.angle_matrix[j, 0]) / np.abs(
                        self.solver.angular_velocity_matrix[j, 0])
                else:
                    time_spent += self.animation_speed
            end_drawing_time = time.time()
            totall_time = np.heaviside(time_spent - (end_drawing_time - start_drawing_time), 0) * (
                        time_spent - (end_drawing_time - start_drawing_time))
            if totall_time > self.animation_speed:
                totall_time = self.animation_speed / 4
            time.sleep(totall_time / self.animation_speed)
            QtWidgets.QApplication.processEvents()
            start_step = end_step

    # *********************************************
    # ******* when we animate something...*********
    # *********************************************

    def draw_links(self, i):
        start_pos_loop_1 = [0, 0]
        self.dynamic_ax_animation.clear()
        # draw vector 2 and 3 and 4
        for vector_index in range(0, 3):
            end_pos_loop_1 = [
                self.vectors[vector_index].length * np.cos(np.radians(self.solver.angle_matrix[i, vector_index])),
                self.vectors[vector_index].length * np.sin(np.radians(self.solver.angle_matrix[i, vector_index]))]
            rect_loop_1 = mpatches.Rectangle(start_pos_loop_1, self.vectors[vector_index].length, self.link_thickness,
                                             angle=self.solver.angle_matrix[i, vector_index], ec="none", linewidth=0,
                                             facecolor=self.color_code[vector_index])
            self.patches[vector_index] = rect_loop_1
            start_pos_loop_1[0] = end_pos_loop_1[0] + start_pos_loop_1[0] - self.link_thickness / 2 * np.sin(
                np.radians(self.solver.angle_matrix[i, vector_index])) + self.link_thickness / 2 * np.sin(
                np.radians(self.solver.angle_matrix[i, vector_index + 1]))
            start_pos_loop_1[1] = end_pos_loop_1[1] + start_pos_loop_1[1] + self.link_thickness / 2 * np.cos(
                np.radians(self.solver.angle_matrix[i, vector_index])) - self.link_thickness / 2 * np.cos(
                np.radians(self.solver.angle_matrix[i, vector_index + 1]))
            QtWidgets.QApplication.processEvents()

        # --------------------------------
        # draw vector 5 and 6
        start_pos_loop_2 = [self.vectors[6].length - self.vectors[7].length, 0]
        for vector_index in reversed(range(3, 5)):
            end_pos_loop_2 = [
                self.vectors[vector_index].length * np.cos(np.radians(self.solver.angle_matrix[i, vector_index])),
                self.vectors[vector_index].length * np.sin(np.radians(self.solver.angle_matrix[i, vector_index]))]
            rect_loop_2 = mpatches.Rectangle(start_pos_loop_2, self.vectors[vector_index].length, self.link_thickness,
                                             angle=self.solver.angle_matrix[i, vector_index], ec="none", linewidth=0,
                                             facecolor=self.color_code[vector_index])
            self.patches[vector_index] = rect_loop_2

            if vector_index == 3:
                x_correction = - self.link_thickness / 2 * np.sin(
                    np.radians(self.solver.angle_matrix[i, vector_index])) + self.link_thickness / 2 * np.sin(
                    np.radians(self.solver.angle_matrix[i, vector_index + 1]))

                y_correction = + self.link_thickness / 2 * np.cos(
                    np.radians(self.solver.angle_matrix[i, vector_index])) - self.link_thickness / 2 * np.cos(
                    np.radians(self.solver.angle_matrix[i, vector_index + 1]))
            else:
                x_correction = + self.link_thickness / 2 * np.sin(
                    np.radians(self.solver.angle_matrix[i, vector_index - 1]))

                y_correction = - self.link_thickness / 2 * np.cos(
                    np.radians(self.solver.angle_matrix[i, vector_index - 1]))

            start_pos_loop_2[0] = end_pos_loop_2[0] + start_pos_loop_2[0] + x_correction
            start_pos_loop_2[1] = end_pos_loop_2[1] + start_pos_loop_2[1] + y_correction
            QtWidgets.QApplication.processEvents()

        # draw path of P
        p_coordinates = [self.solver.p_coordinates_matrix[i, 0], self.solver.p_coordinates_matrix[i, 1]]
        z_coordinates = [self.solver.z_coordinates_matrix[i, 0], self.solver.z_coordinates_matrix[i, 1]]
        circle_1 = mpatches.Circle(p_coordinates, radius=self.link_thickness / 5, ec="none", linewidth=0,
                                   facecolor=self.color_code[0])
        self.patches.append(circle_1)

        circle_2 = mpatches.Circle(z_coordinates, radius=self.link_thickness / 5, ec="none", linewidth=0,
                                   facecolor=self.color_code[1])
        self.patches.append(circle_2)

        collection = PatchCollection(self.patches, alpha=1, match_original=True)
        self.dynamic_ax_animation.add_collection(collection)
        self.dynamic_ax_animation.axis('equal')
        self.dynamic_ax_animation.axis('off')
        self.dynamic_ax_animation.figure.canvas.draw()

    def export_excel(self):
        """ At first We make distance project directory and then we make """
        self.overall_folder_path = "Overall"
        self.point_p_folder_path = "Point P"
        self.point_z_folder_path = "Point Z"
        self.project_path = "project"
        self.export_step = int(self.show_step / self.step)
        self.specify_location(self.project_path + "/" + self.overall_folder_path)
        self.specify_location(self.project_path + "/" + self.point_p_folder_path)
        self.specify_location(self.project_path + "/" + self.point_z_folder_path)

        # ********************************
        # **********overall tables********
        # ********************************
        self.overall_file_names = (
        "Angles", "Angular-Velocities", "Angular-Acceleration", "Theta-Prime", "Theta-Double-Prime", "Determinants")
        self.overall_matrixes = (
        self.solver.angle_matrix, self.solver.angular_velocity_matrix, self.solver.angular_acceleration_matrix,
        self.solver.theta_prime_matrix, self.solver.theta_zegond_matrix, self.solver.matrix_det_of_coefficients)
        self.overall_headers = [["Theta 2", "Theta 3", "Theta 4", "Theta 5", "Theta 6"],
                                ["Theta 2", "Omega 2", "Omega 3", "Omega 4", "Omega 5", "Omega 6"],
                                ["Theta 2", "Alpha 2", "Alpha 3", "Alpha 4", "Alpha 5", "Alpha 6"],
                                ["Theta 2", "Theta prime 2", "Theta prime 3", "Theta prime 4", "Theta prime 5",
                                 "Theta prime 6"],
                                ["Theta 2", "Theta double prime 2", "Theta double prime 3", "Theta double prime 4",
                                 "Theta double prime 5", "Theta double prime 6"],
                                ["Theta2", "Det Loop 1", "Det Loop 2"]]

        for excel_number in range(0, 6):
            file = open(self.project_path + "/" + self.overall_folder_path + "/" + self.overall_file_names[
                excel_number] + '.csv', 'w', newline='')
            with file:
                writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(self.overall_headers[excel_number])
                for i in range(0, self.repeats, self.export_step):
                    if excel_number is not 0 and excel_number is not 5:
                        print(excel_number)
                        new_row = [self.overall_matrixes[0][i, 0]]
                        for j in range(0, 5):
                            new_row.append(self.overall_matrixes[excel_number][i, j])
                        writer.writerow(new_row)
                    elif excel_number is 5:
                        new_row = [self.overall_matrixes[0][i, 0]]
                        for j in range(0, 2):
                            new_row.append(self.overall_matrixes[excel_number][i, j])
                        writer.writerow(new_row)
                    else:
                        writer.writerow(self.overall_matrixes[excel_number][i])

        # ********************************
        # ********** Point P tables*******
        # ********************************
        self.p_point_file_names = (
            "P-Coordinates", "P-Velocities", "P-Acceleration", "P-First-Order-Kinematic-coefficients", "P-Second-Order-Kinematic-coefficients", "P-Center-of-Curvature", "P-Radius-of-Curvature", "P-Tangential-Vector", "P-Normal-Vector")
        self.p_point_matrixes = (
            self.solver.p_coordinates_matrix, self.solver.p_velocity_matrix, self.solver.p_acceleration_matrix,
            self.solver.p_prime_matrix, self.solver.p_zegond_matrix, self.solver.p_center_of_curvature_matrix, self.solver.p_radius_of_curvature_matrix, self.solver.p_tangential_vector_matrix, self.solver.p_normal_vector_matrix)
        self.p_point_headers = [["Theta 2", "x coordinate", "y coordinate"],
                                ["Theta 2", "Vx", "Vy"],
                                ["Theta 2", "ax", "ay"],
                                ["Theta 2", "X'", "Y'"],
                                ["Theta 2", 'X"', 'Y"'],
                                ["Theta 2", 'Cx', 'Cy'],
                                ["Theta 2", 'R'],
                                ["Theta 2", 'Tx', 'Ty'],
                                ["Theta 2", 'Nx', 'Ny']]

        for excel_number in range(0, 9):
            file = open(self.project_path + "/" + self.point_p_folder_path + "/" + self.p_point_file_names[
                excel_number] + '.csv', 'w', newline='')
            with file:
                writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(self.p_point_headers[excel_number])
                for i in range(0, self.repeats, self.export_step):
                    if excel_number is not 6:
                        new_row = [self.overall_matrixes[0][i, 0]]
                        for j in range(0, 2):
                            new_row.append(self.p_point_matrixes[excel_number][i, j])
                        writer.writerow(new_row)
                    else:
                        new_row = [self.overall_matrixes[0][i, 0]]
                        new_row.append(self.p_point_matrixes[excel_number][i, 0])
                        writer.writerow(new_row)
            # ********************************
            # ********** Point P tables*******
            # ********************************
            self.p_point_file_names = (
                "P-Coordinates", "P-Velocities", "P-Acceleration", "P-First-Order-Kinematic-coefficients",
                "P-Second-Order-Kinematic-coefficients", "P-Center-of-Curvature", "P-Radius-of-Curvature",
                "P-Tangential-Vector", "P-Normal-Vector", "P_distance")
            self.p_point_matrixes = (
                self.solver.p_coordinates_matrix, self.solver.p_velocity_matrix, self.solver.p_acceleration_matrix,
                self.solver.p_prime_matrix, self.solver.p_zegond_matrix, self.solver.p_center_of_curvature_matrix,
                self.solver.p_radius_of_curvature_matrix, self.solver.p_tangential_vector_matrix,
                self.solver.p_normal_vector_matrix)
            self.p_point_headers = [["Theta 2", "x coordinate", "y coordinate"],
                                    ["Theta 2", "Vx", "Vy"],
                                    ["Theta 2", "ax", "ay"],
                                    ["Theta 2", "X'", "Y'"],
                                    ["Theta 2", 'X"', 'Y"'],
                                    ["Theta 2", 'Cx', 'Cy'],
                                    ["Theta 2", 'R'],
                                    ["Theta 2", 'Tx', 'Ty'],
                                    ["Theta 2", 'Nx', 'Ny'],
                                    ["Distance_traveled"]]

            for excel_number in range(0, 10):
                if excel_number is not 9:
                    file = open(self.project_path + "/" + self.point_p_folder_path + "/" + self.p_point_file_names[
                        excel_number] + '.csv', 'w', newline='')
                    with file:
                        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(self.p_point_headers[excel_number])
                        for i in range(0, self.repeats, self.export_step):
                            if excel_number is not 6:
                                new_row = [self.overall_matrixes[0][i, 0]]
                                for j in range(0, 2):
                                    new_row.append(self.p_point_matrixes[excel_number][i, j])
                                writer.writerow(new_row)
                            else:
                                new_row = [self.overall_matrixes[0][i, 0], self.p_point_matrixes[excel_number][i, 0]]
                                writer.writerow(new_row)
                elif excel_number is 9:
                    distance = np.zeros(1)
                    distance[0] = self.solver.calculate_p_z_distance(self.solver.p_coordinates_matrix)
                    np.savetxt(self.project_path + "/" + self.point_p_folder_path + "/" + self.p_point_file_names[
                        excel_number] + '.txt', distance)
            # ********************************
            # ********** Point P tables*******
            # ********************************

            self.z_point_file_names = (
                "Z-Coordinates", "Z-Velocities", "Z-Acceleration", "Z-First-Order-Kinematic-coefficients", "Z-Second-Order-Kinematic-coefficients", "Z-Center-of-Curvature", "Z-Radius-of-Curvature", "Z-Tangential-Vector", "Z-Normal-Vector", "Z-distance-traveled")
            self.z_point_matrixes = (
                self.solver.z_coordinates_matrix, self.solver.z_velocity_matrix, self.solver.z_acceleration_matrix,
                self.solver.z_prime_matrix, self.solver.z_zegond_matrix, self.solver.z_center_of_curvature_matrix, self.solver.z_radius_of_curvature_matrix, self.solver.z_tangential_vector_matrix, self.solver.z_normal_vector_matrix)
            self.z_point_headers = [["Theta 2", "x coordinate", "y coordinate"],
                                    ["Theta 2", "Vx", "Vy"],
                                    ["Theta 2", "ax", "ay"],
                                    ["Theta 2", "X'", "Y'"],
                                    ["Theta 2", 'X"', 'Y"'],
                                    ["Theta 2", 'Cx', 'Cy'],
                                    ["Theta 2", 'R'],
                                    ["Theta 2", 'Tx', 'Ty'],
                                    ["Theta 2", 'Nx', 'Ny'],
                                    ["Distance_traveled"]]

            for excel_number in range(0, 10):
                if excel_number is not 9:
                    file = open(self.project_path + "/" + self.point_z_folder_path + "/" + self.z_point_file_names[
                        excel_number] + '.csv', 'w', newline='')
                    with file:
                        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(self.z_point_headers[excel_number])
                        for i in range(0, self.repeats, self.export_step):
                            if excel_number is not 6:
                                new_row = [self.overall_matrixes[0][i, 0]]
                                for j in range(0, 2):
                                    new_row.append(self.z_point_matrixes[excel_number][i, j])
                                writer.writerow(new_row)
                            else:
                                new_row = [self.overall_matrixes[0][i, 0], [self.z_point_matrixes[excel_number][i, 0]]]
                                writer.writerow(new_row)
                elif excel_number is 9:
                    distance = np.zeros(1)
                    distance[0] = self.solver.calculate_p_z_distance(self.solver.z_coordinates_matrix)
                    np.savetxt(self.project_path + "/" + self.point_z_folder_path + "/" + self.z_point_file_names[
                        excel_number] + '.txt', distance)


    def specify_location(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                QMessageBox.warning(self, "An Error Occurred",
                                    "Error occurred while creating directory! Please choose another folder")
        else:
            try:
                shutil.rmtree(path)  # removes all the subdirectories!
                os.makedirs(path)
            except:
                QMessageBox.warning(self, "An Error Occurred",
                                    "Error while creating directory! Please choose another folder")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindowEXEC()
