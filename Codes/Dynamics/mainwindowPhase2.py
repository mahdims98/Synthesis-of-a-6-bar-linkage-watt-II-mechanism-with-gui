from SolverClass import *
from mainwindowguiPhase2 import *
from mainwindowgui_manualPhase2 import *
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
        self.scene_link_2 = QGraphicsScene()
        self.graphicsView_link_2.setScene(self.scene_link_2)

        self.scene_link_3 = QGraphicsScene()
        self.graphicsView_link_3.setScene(self.scene_link_3)

        self.scene_link_4 = QGraphicsScene()
        self.graphicsView_link_4.setScene(self.scene_link_4)

        self.scene_link_5 = QGraphicsScene()
        self.graphicsView_link_5.setScene(self.scene_link_5)

        self.scene_link_6 = QGraphicsScene()
        self.graphicsView_link_6.setScene(self.scene_link_6)

        self.scenes = {2: self.scene_link_2, 3: self.scene_link_3, 4: self.scene_link_4, 5: self.scene_link_5, 6: self.scene_link_6}

        self.blackBrash = QBrush(Qt.black)
        self.fixedBrush = QBrush(Qt.black,Qt.FDiagPattern)
        self.pinBrush = QBrush(Qt.black, Qt.FDiagPattern)
        self.momentumBrush = QBrush(Qt.black,Qt.NoBrush)
        self.blackPen = QPen(Qt.black)
        self.bluePen = QPen(Qt.blue)
        self.bluePen2 = QPen(Qt.blue)
        self.redPen = QPen(Qt.red)
        self.redPen2 = QPen(Qt.red)
        self.yellowPen2 = QPen(Qt.yellow)
        self.blackPen2 = QPen(Qt.black)
        self.blackPen2.setWidth(2)
        self.redPen2.setWidth(2)
        self.yellowPen2.setWidth(2)
        self.bluePen2.setWidth(2)
        self.grayPen2 = QPen(Qt.darkGray)
        self.grayPen2.setWidth(2)
        self.darkBluePen2 = QPen(Qt.darkCyan)
        self.darkBluePen2.setWidth(2)
        self.darkRedPen2 = QPen(Qt.darkRed)
        self.darkRedPen2.setWidth(2)
        self.force_view_scale = 1.2
        self.momentum_view_scale = 40
        self.distributed_view_scale = 10
        self.beam_view_length = 400
        self.beam_view_thickness = 10
        self.link_sketch_scale = 2500
        self.space = self.beam_view_length + 50

        self.fbd_angle = 10

        self.g = 9.81


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
        self.lineEdit_angle[5].setText("291.5")

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

        self.fbd_angle = self.doubleSpinBox_fbd_angle.value()


        step = self.doubleSpinBox_steps.value()
        repeats = self.spinBox_repeats.value()



        vector_1 = KnownVector(length=0.2032, mass=0, inertia=0, angle=180)  # mass and inertial is equal to zero
        vector_2 = KnownVector(length=0.05715, mass=2, inertia=0.0067, angle=0, acceleration_ratio=1)
        vector_3 = UnKnownVector(length=0.18415, mass=5.5, inertia=0.0433)
        vector_4 = UnKnownVector(length=0.1778, mass=2, inertia=0.2426)
        vector_4_prime = UnKnownVector(length=0.127, mass=0,
                                       inertia=0)  ###### mass and inertial actually is not 0. just for debug
        vector_1_prime = KnownVector(length=0.1016, mass=0, inertia=0, angle=180)
        vector_5 = UnKnownVector(length=0.0508, mass=1.5, inertia=0.0009)
        vector_6 = UnKnownVector(length=0.127, mass=6, inertia=0.0634)
        spring = Spring(k=5000, free_length=0.15, max_deflection=0.002896)
        damper = Damper(damping_coefficient=350)

        self.vectors = {2: vector_2, 3:vector_3, 4: vector_4, 5: vector_5, 6: vector_6}

        for vector_index in self.vectors:
            self.create_beam(self.scenes[vector_index], self.vectors[vector_index].length)

        initial_guess_loop_1 = np.array([63.95, 291.5])
        initial_guess_loop_2 = np.array([140, 42.3])

        animation_step = 10

        solver = SixLinkSolver(known_vectors=(vector_1, vector_1_prime, vector_2),
                               unknown_vectors=(vector_3, vector_4, vector_4_prime, vector_5, vector_6),
                               initial_guesses=(initial_guess_loop_1, initial_guess_loop_2), steps=step,
                               num_of_repeats=repeats, spring=spring, damper=damper)
        solver.calculate_angular_properties()

        solver.writer_for_newton_method.save()
        solver.writer_for_static.save()
        solver.writer_for_energy.save()

        self.fbd_angle = int(self.fbd_angle/step)

        vector_2.start_force.x_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 0])
        vector_2.start_force.y_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 1])
        vector_2.end_force.x_force = + float(solver.dynamic_method_forces_matrix[self.fbd_angle, 2])
        vector_2.end_force.y_force = + float(solver.dynamic_method_forces_matrix[self.fbd_angle, 3])

        vector_3.start_force.x_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 2])
        vector_3.start_force.y_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 3])
        vector_3.end_force.x_force = + float(solver.dynamic_method_forces_matrix[self.fbd_angle, 4])
        vector_3.end_force.y_force = + float(solver.dynamic_method_forces_matrix[self.fbd_angle, 5])

        vector_4.start_force.x_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 4])
        vector_4.start_force.y_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 5])
        vector_4.end_force.x_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 8])
        vector_4.end_force.y_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 9])

        vector_5.start_force.x_force = - float(solver.dynamic_method_forces_matrix[self.fbd_angle, 10])
        vector_5.start_force.y_force = - float(solver.dynamic_method_forces_matrix[self.fbd_angle, 11])
        vector_5.end_force.x_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 6])
        vector_5.end_force.y_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 7])

        vector_6.start_force.x_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 12])
        vector_6.start_force.y_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 13])
        vector_6.end_force.x_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 10])
        vector_6.end_force.y_force = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 11])


        vector_2.momentum = float(solver.dynamic_method_forces_matrix[self.fbd_angle, 14])
        self.vectors = {2: vector_2, 3: vector_3, 4: vector_4, 5: vector_5, 6: vector_6}

        for vector_index in self.vectors:
            # draw start and end forces
            self.draw_x_force(scene=self.scenes[vector_index], point_force_position=0, point_force_magnitude=np.abs(self.vectors[vector_index].start_force.x_force), point_force_sign=np.sign(self.vectors[vector_index].start_force.x_force), pen=self.redPen2)
            self.draw_x_force(scene=self.scenes[vector_index], point_force_position=self.vectors[vector_index].length,
                              point_force_magnitude=np.abs(self.vectors[vector_index].end_force.x_force),
                              point_force_sign=np.sign(self.vectors[vector_index].end_force.x_force),
                              pen=self.redPen2)

            self.draw_y_force(scene=self.scenes[vector_index], point_force_position=0, point_force_magnitude=np.abs(self.vectors[vector_index].start_force.y_force), point_force_sign=np.sign(self.vectors[vector_index].start_force.y_force), pen=self.redPen2)
            self.draw_y_force(scene=self.scenes[vector_index], point_force_position=self.vectors[vector_index].length,
                              point_force_magnitude=np.abs(self.vectors[vector_index].end_force.y_force),
                              point_force_sign=np.sign(self.vectors[vector_index].end_force.y_force),
                              pen=self.redPen2)

            # draw mass force
            if vector_index is 2 or vector_index is 6:
                self.draw_y_force(scene=self.scenes[vector_index], point_force_position=0.0001,
                                  point_force_magnitude=np.abs(self.vectors[vector_index].mass * self.g),
                                  point_force_sign=-1,
                                  pen=self.yellowPen2)
            elif vector_index is 4:
                self.draw_y_force(scene=self.scenes[vector_index], point_force_position=self.vectors[vector_index].length,
                                  point_force_magnitude=np.abs(self.vectors[vector_index].mass * self.g),
                                  point_force_sign=-1,
                                  pen=self.yellowPen2)
            else:
                self.draw_y_force(scene=self.scenes[vector_index], point_force_position=self.vectors[vector_index].length/2,
                                  point_force_magnitude=np.abs(self.vectors[vector_index].mass * self.g),
                                  point_force_sign=-1,
                                  pen=self.yellowPen2)

            # draw angular acceleration

            if vector_index is 2 or vector_index is 6:
                self.draw_momentum(scene=self.scenes[vector_index], momentum_position=0,
                                  momentum_magnitude= np.abs(solver.angular_acceleration_matrix[self.fbd_angle, vector_index-2] * self.vectors[vector_index].inertia),
                                  momentum_sign=  -np.sign(solver.angular_acceleration_matrix[self.fbd_angle, vector_index-2] * self.vectors[vector_index].inertia),
                                  pen=self.darkBluePen2)
            elif vector_index is 4:
                self.draw_momentum(scene=self.scenes[vector_index], momentum_position=self.vectors[vector_index].length,
                                  momentum_magnitude= np.abs(solver.angular_acceleration_matrix[self.fbd_angle, vector_index-2] * self.vectors[vector_index].inertia),
                                  momentum_sign=  - np.sign(solver.angular_acceleration_matrix[self.fbd_angle, vector_index-2] * self.vectors[vector_index].inertia),
                                  pen=self.darkBluePen2)

            else:
                self.draw_momentum(scene=self.scenes[vector_index], momentum_position=self.vectors[vector_index].length/2,
                                  momentum_magnitude= np.abs(solver.angular_acceleration_matrix[self.fbd_angle, vector_index-2] * self.vectors[vector_index].inertia),
                                  momentum_sign=  - np.sign(solver.angular_acceleration_matrix[self.fbd_angle, vector_index-2] * self.vectors[vector_index].inertia),
                                  pen=self.darkBluePen2)

            # draw input momentum

            self.draw_momentum(scene=self.scenes[2], momentum_position=0,
                               momentum_magnitude=np.abs(self.vectors[2].momentum),
                               momentum_sign=np.sign(self.vectors[2].momentum),
                               pen=self.grayPen2)

            # draw vector 5 forces on vector 4

            self.draw_x_force(scene=self.scenes[4], point_force_position=vector_4.length - vector_4_prime.length,
                              point_force_magnitude=np.abs(self.vectors[5].end_force.x_force),
                              point_force_sign=np.sign(self.vectors[5].end_force.x_force),
                              pen=self.redPen2)

            self.draw_y_force(scene=self.scenes[4], point_force_position=vector_4.length - vector_4_prime.length,
                              point_force_magnitude=np.abs(self.vectors[5].end_force.y_force),
                              point_force_sign=np.sign(self.vectors[5].end_force.y_force),
                              pen=self.redPen2)

            # draw aG on vector 5

            self.draw_x_force(scene=self.scenes[5], point_force_position=vector_5.length/2,
                              point_force_magnitude=np.abs(solver.p_acceleration_matrix[self.fbd_angle, 0] * self.vectors[5].mass),
                              point_force_sign= - np.sign(solver.p_acceleration_matrix[self.fbd_angle, 0] * self.vectors[5].mass),
                              pen=self.darkBluePen2)

            self.draw_y_force(scene=self.scenes[5], point_force_position=vector_5.length/2,
                              point_force_magnitude=np.abs(solver.p_acceleration_matrix[self.fbd_angle, 1] * self.vectors[5].mass),
                              point_force_sign= - np.sign(solver.p_acceleration_matrix[self.fbd_angle, 1] * self.vectors[5].mass),
                              pen=self.darkBluePen2)

            # draw aG on vector 3

            self.draw_x_force(scene=self.scenes[3], point_force_position=vector_3.length/2,
                              point_force_magnitude=np.abs(solver.vector_3_cg_acceleration_matrix[self.fbd_angle, 0] * self.vectors[3].mass),
                              point_force_sign= - np.sign(solver.vector_3_cg_acceleration_matrix[self.fbd_angle, 0] * self.vectors[3].mass),
                              pen=self.darkBluePen2)

            self.draw_y_force(scene=self.scenes[3], point_force_position=vector_3.length/2,
                              point_force_magnitude=np.abs(solver.vector_3_cg_acceleration_matrix[self.fbd_angle, 1] * self.vectors[3].mass),
                              point_force_sign= - np.sign(solver.vector_3_cg_acceleration_matrix[self.fbd_angle, 1] * self.vectors[3].mass),
                              pen=self.darkBluePen2)






    def draw_beam(self, scene: QGraphicsScene,  start_pos, end_pos, length, thickness):
        scene.addRect(start_pos, end_pos, length, thickness, self.blackPen,
                                  self.blackBrash)

    def draw_y_force(self, scene, point_force_position, point_force_magnitude, point_force_sign, pen):
        if point_force_sign == -1:
            scene.addLine(point_force_position * self.link_sketch_scale, 0,
                                      point_force_position * self.link_sketch_scale, point_force_sign * self.force_view_scale * point_force_magnitude, pen)
            scene.addLine(point_force_position * self.link_sketch_scale, 0,
                                      point_force_position * self.link_sketch_scale - 5, -5, pen)
            scene.addLine(point_force_position * self.link_sketch_scale, 0,
                                      point_force_position * self.link_sketch_scale + 5, -5, pen)
        else:
            scene.addLine(point_force_position * self.link_sketch_scale, point_force_sign * self.beam_view_thickness,
                                      point_force_position * self.link_sketch_scale, point_force_sign * self.force_view_scale * point_force_magnitude + point_force_sign * self.beam_view_thickness, pen)
            scene.addLine(point_force_position * self.link_sketch_scale, point_force_sign * self.beam_view_thickness,
                                      point_force_position * self.link_sketch_scale + 5, point_force_sign * self.beam_view_thickness + 5, pen)
            scene.addLine(point_force_position * self.link_sketch_scale, point_force_sign * self.beam_view_thickness,
                                      point_force_position * self.link_sketch_scale - 5, point_force_sign * self.beam_view_thickness + 5, pen)

    def draw_x_force(self, scene, point_force_position, point_force_magnitude, point_force_sign, pen):
        if point_force_sign == -1:
            scene.addLine(point_force_position * self.link_sketch_scale, self.beam_view_thickness/2,
                                      point_force_position * self.link_sketch_scale + self.force_view_scale * point_force_magnitude, self.beam_view_thickness/2, pen)
            scene.addLine(point_force_position * self.link_sketch_scale, self.beam_view_thickness/2,
                                      point_force_position * self.link_sketch_scale + 5, self.beam_view_thickness/2 -5, pen)
            scene.addLine(point_force_position * self.link_sketch_scale, self.beam_view_thickness/2,
                                      point_force_position * self.link_sketch_scale + 5, self.beam_view_thickness/2 +5, pen)
        else:
            scene.addLine(point_force_position * self.link_sketch_scale, self.beam_view_thickness/2,
                                      point_force_position * self.link_sketch_scale + self.force_view_scale * point_force_magnitude, self.beam_view_thickness/2, pen)
            scene.addLine(point_force_position * self.link_sketch_scale + self.force_view_scale * point_force_magnitude, self.beam_view_thickness/2,
                                      point_force_position * self.link_sketch_scale + self.force_view_scale * point_force_magnitude -5, self.beam_view_thickness/2 -5, pen)
            scene.addLine(point_force_position * self.link_sketch_scale + self.force_view_scale * point_force_magnitude, self.beam_view_thickness/2,
                                      point_force_position * self.link_sketch_scale + self.force_view_scale * point_force_magnitude - 5, self.beam_view_thickness/2 +5, pen)

    def draw_momentum(self, scene,  momentum_position, momentum_magnitude, momentum_sign, pen):
        scene.addEllipse(momentum_position * self.link_sketch_scale - momentum_magnitude * self.momentum_view_scale / 2,
                                     (self.beam_view_thickness-momentum_magnitude*self.momentum_view_scale) / 2,
                                     momentum_magnitude * self.momentum_view_scale, momentum_magnitude * self.momentum_view_scale, pen, self.momentumBrush)
        scene.addLine(momentum_position * self.link_sketch_scale,
                                  (self.beam_view_thickness-momentum_magnitude*self.momentum_view_scale) / 2,
                                  momentum_position * self.link_sketch_scale - momentum_sign * 5,
                                  (self.beam_view_thickness-momentum_magnitude*self.momentum_view_scale) / 2 - momentum_sign * 5, pen)
        scene.addLine(momentum_position * self.link_sketch_scale,
                                  (self.beam_view_thickness-momentum_magnitude*self.momentum_view_scale) / 2,
                                  momentum_position * self.link_sketch_scale - momentum_sign * 5,
                                  (self.beam_view_thickness-momentum_magnitude*self.momentum_view_scale) / 2 + momentum_sign * 5, pen)

    def create_beam(self,scene, link_length):
        link_length_scaled = link_length * self.link_sketch_scale
        self.draw_beam(scene, 0, 0, link_length_scaled, self.beam_view_thickness)










if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindowEXEC()
