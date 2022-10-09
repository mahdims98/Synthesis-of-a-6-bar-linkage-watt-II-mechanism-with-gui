import numpy as np
from scipy.optimize import fsolve
from typing import Tuple
from PyQt5 import QtWidgets
from numpy import array
from numpy import linalg as la
import math
import os
import shutil
import csv
from pandas import ExcelWriter, DataFrame
from sympy import Eq, Symbol, solve




class Spring:
    def __init__(self, k, free_length, max_deflection=None):
        """ this class represent a spring
        """
        self.k = k
        self.free_length = free_length
        self.force = None
        self.max_deflection = max_deflection



class Damper:
    def __init__(self, damping_coefficient):
        """ this class represent a spring
        """
        self.damping_coefficient = damping_coefficient
        self.force = None


class Force:
    def __init__(self):
        """ this class represent a force vector that has two dimensions
        """
        self.x_force = None
        self.y_force = None

    def get_force_angle(self):
        return np.arctan(self.y_force / self.x_force)

    def get_force_magnitude(self):
        return np.sqrt(self.x_force**2 + self.y_force**2)


class Point:
    def __init__(self):
        """ this class represent a point like point P and point Z
        """
        self.x_coordinate = None
        self.y_coordinate = None
        self.x_velocity = 0
        self.y_velocity = 0
        self.x_acceleration = 0
        self.y_acceleration = 0
        self.x_prime = 0
        self.y_prime = 0
        self.x_double_prime = 0
        self.y_double_prime = 0
        self.theta_prime = 0
        self.theta_double_prime = 0


class CenterOfMass(Point):
    pass


class Vector:
    def __init__(self, length: float, mass: float, inertia: float):
        """ this class represent a vector that has length and angle between vector direction and positive direction
        of x axis
        :param float length: vector length in (m)
        :param float inertia: moment of inertia kg.m^2
        :param float mass: mass in kg
        """
        self.length = length
        self.inertia = inertia
        self.mass = mass
        self.angle = None
        self.angular_acceleration = None
        self.CG_acceleration_x = None
        self.CG_acceleration_y = None
        self.angular_velocity = None
        self.theta_prime = None
        self.theta_zegond = None
        self.start_force = Force()
        self.end_force = Force()
        self.cg = CenterOfMass()
        self.a = None
        self.b = None


        self.compressive_yield_strength = 420 *10**6
        self.module_of_elasticity = 200 * 10**9
        self.sr_d = np.pi * np.sqrt(2 * 1 * (self.module_of_elasticity) / self.compressive_yield_strength)
        self.minimum_r = -np.inf

        self.momentum = None


class KnownVector(Vector):
    def __init__(self, length: float, mass: float, inertia: float, angle: float, acceleration_ratio=1):
        """ this class represent a vector that has length and angle between vector direction and positive direction
        of x axis
        :param float angle: angle in degrees, angle between vector and positive direction of vector
        :param float length: vector length in (m)
        """
        super().__init__(length, mass, inertia)
        self.angle = angle
        self.acceleration_ratio = acceleration_ratio
        self.update_theta(angle)


    def update_theta(self, new_theta):
        if new_theta > 360:
            self.angle = new_theta - 360
        else:
            self.angle = new_theta

        self.angle = np.round(self.angle, 3)

        if 0 <= self.angle < 50:
            self.angular_acceleration = -5 * np.pi * self.acceleration_ratio
            self.angular_velocity = np.sqrt(((-5 * np.pi * self.angular_acceleration) / 9) * (1 - (self.angle / 50)))

        elif 50 <= self.angle < 150:
            self.angular_acceleration = +6 * np.pi * self.acceleration_ratio
            self.angular_velocity = np.sqrt(((10 * np.pi * self.angular_acceleration) / 9) * ((self.angle - 50) / 100))

        elif 150 <= self.angle < 250:
            self.angular_acceleration = -6 * np.pi * self.acceleration_ratio
            self.angular_velocity = np.sqrt(
                ((-10 * np.pi * self.angular_acceleration) / 9) * (1 - ((self.angle - 150) / 100)))

        elif 250 <= self.angle < 330:
            self.angular_acceleration = +5 * np.pi * self.acceleration_ratio
            self.angular_velocity = np.sqrt(((8 * np.pi * self.angular_acceleration) / 9) * ((self.angle - 250) / 80))

        elif 330 <= self.angle < 360:
            self.angular_acceleration = -5 * np.pi * self.acceleration_ratio
            self.angular_velocity = np.sqrt(
                ((-8 * np.pi * self.angular_acceleration) / 9) * (1 - ((self.angle - 330) / 80)))


class UnKnownVector(Vector):
    pass


class FourLinkSolver:
    """
    this class can solve a four bar linkage equation. in known vectors, both of angle and lengths are known. angle of
    unknown vectors are unknown but their lengths are known. we have two equations in x direction and y direction. first
    we have to set inputs which are two objects of KnownVector and two objects of UnKnownVector. finally we have initial
    guess.

    ******input angles are all in degrees!********

    :param tuple known_vectors: two object of KnownVector [Vector 2, Vector 1 (fixed to earth)]
    :param tuple unknown_vectors: two object of UnKnownVector
    :param np.ndarray initial_guesses: two initial guesses of two unknown angles. must be in Degree
    """

    def __init__(self, known_vectors: Tuple[Vector, Vector],
                 unknown_vectors: Tuple[UnKnownVector, UnKnownVector], initial_guess: np.ndarray):
        self.known_vector = known_vectors
        self.unknown_vector = unknown_vectors
        self.initial_guess = np.radians(initial_guess)

    def theta_equation(self, unknown_theta: [float, float]):
        """
        function which is used in fsolve
        :param unknown_theta: parameter which is used in fsolve
        """
        self.unknown_vector[0].angle = unknown_theta[0]
        self.unknown_vector[1].angle = unknown_theta[1]

        x_equation = sum(
            known_vector.length * np.cos(np.radians(known_vector.angle)) for known_vector in self.known_vector) + sum(
            unknown_vector.length * np.cos(unknown_vector.angle) for unknown_vector in
            self.unknown_vector)

        y_equation = sum(
            known_vector.length * np.sin(np.radians(known_vector.angle)) for known_vector in self.known_vector) + sum(
            unknown_vector.length * np.sin(unknown_vector.angle) for unknown_vector in
            self.unknown_vector)

        return x_equation, y_equation

    def calculate_theta(self) -> np.ndarray:
        """
        :return: return unknown angles in degrees
        """
        return np.degrees(fsolve(self.theta_equation, self.initial_guess))

    # ---------------------------------------
    # ------angular velocity calculation-----
    # ---------------------------------------

    def calculate_angular_velocity(self) -> Tuple[float, float]:
        """ here we calculate first order coefficients
        a is matrix of coefficients in equation and b is the Ordinate

        :returns: angular velocities of given unknown vectors"""

        a = np.zeros((2, 2))
        for i in range(0, 2):
            a[0, i] = self.unknown_vector[i].length * np.sin(np.radians(self.unknown_vector[i].angle))
        for i in range(0, 2):
            a[1, i] = self.unknown_vector[i].length * np.cos(np.radians(self.unknown_vector[i].angle))

        b = np.zeros((2, 1))
        b[0, 0] = -self.known_vector[0].length * np.sin(np.radians(self.known_vector[0].angle))
        b[1, 0] = -self.known_vector[0].length * np.cos(np.radians(self.known_vector[0].angle))

        self.unknown_vector[0].theta_prime, self.unknown_vector[1].theta_prime = np.linalg.solve(a, b)

        self.unknown_vector[0].angular_velocity = self.unknown_vector[0].theta_prime * self.known_vector[
            0].angular_velocity
        self.unknown_vector[1].angular_velocity = self.unknown_vector[1].theta_prime * self.known_vector[
            0].angular_velocity

        return self.unknown_vector[0].angular_velocity, self.unknown_vector[1].angular_velocity

    # ---------------------------------------
    # ------angular acceleration calculation----
    # ---------------------------------------

    def calculate_angular_acceleration(self) -> Tuple[float, float]:
        """ here we calculate second order coefficients
        a is matrix of coefficients in equation and b is the Ordinate

        :returns: angular accelerations of given unknown vectors"""

        a = np.zeros((2, 2))
        for i in range(0, 2):
            a[0, i] = self.unknown_vector[i].length * np.sin(np.radians(self.unknown_vector[i].angle))
        for i in range(0, 2):
            a[1, i] = self.unknown_vector[i].length * np.cos(np.radians(self.unknown_vector[i].angle))

        b = np.zeros((2, 1))
        b[0, 0] = -self.known_vector[0].length * np.cos(np.radians(self.known_vector[0].angle)) - sum(
            unknown_vector.length * (unknown_vector.theta_prime ** 2) * np.cos(np.radians(unknown_vector.angle)) for
            unknown_vector in self.unknown_vector)
        b[1, 0] = +self.known_vector[0].length * np.sin(np.radians(self.known_vector[0].angle)) + sum(
            unknown_vector.length * (unknown_vector.theta_prime ** 2) * np.sin(np.radians(unknown_vector.angle)) for
            unknown_vector in self.unknown_vector)

        self.unknown_vector[0].theta_zegond, self.unknown_vector[1].theta_zegond = np.linalg.solve(a, b)

        self.unknown_vector[0].angular_acceleration = self.unknown_vector[0].theta_zegond * (
                self.known_vector[0].angular_velocity ** 2) + self.unknown_vector[0].theta_prime * \
                                                      self.known_vector[0].angular_acceleration
        self.unknown_vector[1].angular_acceleration = self.unknown_vector[1].theta_zegond * (
                self.known_vector[0].angular_velocity ** 2) + self.unknown_vector[1].theta_prime * \
                                                      self.known_vector[0].angular_acceleration

        return self.unknown_vector[0].angular_acceleration, self.unknown_vector[1].angular_acceleration


class SixLinkSolver:
    def __init__(self, known_vectors: Tuple[KnownVector, KnownVector, KnownVector],
                 unknown_vectors: Tuple[UnKnownVector, UnKnownVector, UnKnownVector, UnKnownVector, UnKnownVector],
                 initial_guesses: Tuple[np.ndarray, np.ndarray], num_of_repeats: int, steps: int, spring: Spring,
                 damper: Damper):
        """
        inputs must be in a shape like this:
        :param known_vectors Tuple[vector_1, vector_1_prime, vector_2] which are KnownVector objects
        :param unknown_vectors Tuple[vector_3, vector_4,vector_4_prime vector_5, vector_6] which are UnKnownVector objects
        :param initial_guesses Tuple[initial_guess_loop_1, initial_guess_loop_2] which are np.arrays objects
        :param steps : int , angle steps
        :param num_of_repeats: int, how many loops are needed?
        :param damper Damper
        :param spring Spring
        vector 1 (earth) (O2 - O4)
        vector 1 prime (earth) (O6-o4)
        """
        self.vector_1, self.vector_1_prime, self.vector_2 = known_vectors
        self.vector_3, self.vector_4, self.vector_4_prime, self.vector_5, self.vector_6 = unknown_vectors
        self.initial_guesses = initial_guesses
        self.steps = steps
        self.num_of_repeats = num_of_repeats
        self.spring = spring
        self.damper = damper
        self.safety_factor = 1.5


        self.point_p = Point()
        self.point_z = Point()

        ########################################################
        # tables
        self.show_step = 10

        self.dynamic_method_folder_path = "Dynamic-Newton-method"
        self.static_method_folder_path = "Static-Newton-method"
        self.energy_method_folder_path = "Energy-method"
        self.project_path = "project"
        self.export_step = int(self.show_step / self.steps)
        self.specify_location(self.project_path + "/" + self.dynamic_method_folder_path)
        self.specify_location(self.project_path + "/" + self.static_method_folder_path)
        self.specify_location(self.project_path + "/" + self.energy_method_folder_path)

        self.excel_number_for_forces_dynamic = 5
        self.excel_sheet_names_of_forces_dynamic = ("Link 2", "Link 3", "Link 4", "Link 5", "Link 6", "Spring", "Damper", "Total-Momentum")
        self.excel_names_of_forces_static = ("link-1-forces", "link-2-forces", "link-3-forces", "link-4-forces",
                                             "link-5-forces", "link-6-forces")
        self.excel_headers_of_forces = ["Theta 2", "Fx start", "Fy start", "Fx end", "Fy end"]
        self.row_number_newton_excel = 0
        self.row_number_static_excel = 0
        self.row_number_energy_solver = 0

        self.writer_for_newton_method = ExcelWriter(
            self.project_path + "/" + self.dynamic_method_folder_path + "/" + self.dynamic_method_folder_path + '.xlsx',
            engine='xlsxwriter')

        self.writer_for_static = ExcelWriter(
            self.project_path + "/" + self.static_method_folder_path + "/" + self.static_method_folder_path + '.xlsx',
            engine='xlsxwriter')


        data_frame = DataFrame([self.excel_headers_of_forces])
        data_frame_spring = DataFrame([["Theta2", "Spring force"]])
        data_frame_damper = DataFrame([["Theta2", "Damper force"]])
        data_frame_momentum = DataFrame([["Theta2", "Total-Momentum"]])

        for sheet_name in self.excel_sheet_names_of_forces_dynamic:
            if sheet_name == "Spring":
                data_frame_spring.to_excel(self.writer_for_newton_method, sheet_name=sheet_name, header=None, index=None)
                data_frame_spring.to_excel(self.writer_for_static, sheet_name=sheet_name, header=None,
                                           index=None)
            elif sheet_name == "Damper":
                data_frame_damper.to_excel(self.writer_for_newton_method, sheet_name=sheet_name, header=None,
                                           index=None)
                data_frame_damper.to_excel(self.writer_for_static, sheet_name=sheet_name, header=None,
                                           index=None)
            elif sheet_name == "Total-Momentum":
                data_frame_momentum.to_excel(self.writer_for_newton_method, sheet_name=sheet_name, header=None,
                                           index=None)
                data_frame_momentum.to_excel(self.writer_for_static, sheet_name=sheet_name, header=None,
                                           index=None)
            else:
                data_frame.to_excel(self.writer_for_newton_method, sheet_name=sheet_name, header=None, index=None)
                data_frame.to_excel(self.writer_for_static, sheet_name=sheet_name, header=None, index=None)
        self.row_number_newton_excel += 1
        self.row_number_static_excel += 1

        self.excel_sheet_names_energy_method = ("equivalent inertia", "B", "Total-Momentum")

        self.writer_for_energy = ExcelWriter(
            self.project_path + "/" + self.energy_method_folder_path + "/" + self.energy_method_folder_path + '.xlsx',
            engine='xlsxwriter')

        data_frame_equivalent_inertia = DataFrame([["Theta2", "Sigma A", "A term in momentum Equation"]])
        data_frame_equivalent_inertia.to_excel(self.writer_for_energy, sheet_name=self.excel_sheet_names_energy_method[0], header=None,
                                       index=None)

        data_frame_sigma_b = DataFrame([["Theta2", "Sigma B", "B term in momentum Equation"]])
        data_frame_sigma_b.to_excel(self.writer_for_energy, sheet_name=self.excel_sheet_names_energy_method[1], header=None,
                                       index=None)

        data_frame_momentum = DataFrame([["Theta2", "Total-Momentum"]])
        data_frame_momentum.to_excel(self.writer_for_energy, sheet_name=self.excel_sheet_names_energy_method[2], header=None,
                                       index=None)

        self.row_number_energy_solver += 1

        #########################################################

        self.angle_matrix = np.zeros((self.num_of_repeats, 5))
        self.angular_velocity_matrix = np.zeros((self.num_of_repeats, 5))
        self.angular_acceleration_matrix = np.zeros((self.num_of_repeats, 5))
        self.theta_prime_matrix = np.zeros((self.num_of_repeats, 5))
        self.theta_zegond_matrix = np.zeros((self.num_of_repeats, 5))

        self.p_coordinates_matrix = np.zeros((self.num_of_repeats, 2))
        self.p_velocity_matrix = np.zeros((self.num_of_repeats, 2))
        self.p_acceleration_matrix = np.zeros((self.num_of_repeats, 2))
        self.p_prime_matrix = np.zeros((self.num_of_repeats, 2))
        self.p_zegond_matrix = np.zeros((self.num_of_repeats, 2))
        self.p_center_of_curvature_matrix = np.zeros((self.num_of_repeats, 2))
        self.p_radius_of_curvature_matrix = np.zeros((self.num_of_repeats, 1))

        """ normal or tangential vector has 2 components : I and J direct    """
        self.p_normal_vector_matrix = np.zeros((self.num_of_repeats, 2))
        self.p_tangential_vector_matrix = np.zeros((self.num_of_repeats, 2))

        self.z_coordinates_matrix = np.zeros((self.num_of_repeats, 2))
        self.z_velocity_matrix = np.zeros((self.num_of_repeats, 2))
        self.z_acceleration_matrix = np.zeros((self.num_of_repeats, 2))
        self.z_prime_matrix = np.zeros((self.num_of_repeats, 2))
        self.z_zegond_matrix = np.zeros((self.num_of_repeats, 2))
        self.z_center_of_curvature_matrix = np.zeros((self.num_of_repeats, 2))
        self.z_radius_of_curvature_matrix = np.zeros((self.num_of_repeats, 1))

        """ normal or tangential vector has 2 components : I and J direct    """
        self.z_normal_vector_matrix = np.zeros((self.num_of_repeats, 2))
        self.z_tangential_vector_matrix = np.zeros((self.num_of_repeats, 2))

        self.angle_of_velocity_vector = np.zeros((self.num_of_repeats, 1))

        """
          in this matrix was calculated det of coefficients matrix
          in column one 3 and 4 theta primes
          in column two 5 and 6 theta primes
        """
        self.matrix_det_of_coefficients = np.zeros((self.num_of_repeats, 2))
        """
        for dynamic part 
        """
        self.dynamic_method_forces_matrix = np.zeros((self.num_of_repeats, 15))
        self.static_method_forces_matrix = np.zeros((self.num_of_repeats, 15))
        # for energy method

        self.energy_calculated_momentum = np.zeros((self.num_of_repeats, 1))
        self.equivalent_inertia_matrix = np.zeros((self.num_of_repeats, 1))
        self.sigma_b_matrix = np.zeros((self.num_of_repeats, 1))
        self.sigma_a_energy_term_matrix = np.zeros((self.num_of_repeats, 1))
        self.sigma_b_energy_term_matrix = np.zeros((self.num_of_repeats, 1))
        self.sigma_potential_term_matrix = np.zeros((self.num_of_repeats, 1))
        self.energy_method_spring_term_matrix = np.zeros((self.num_of_repeats, 1))
        self.energy_method_damper_term_matrix = np.zeros((self.num_of_repeats, 1))

        self.vector_3_cg_acceleration_matrix = np.zeros((self.num_of_repeats, 2))
    @staticmethod
    def specify_location(path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                print("An Error Occurred")
        else:
            try:
                shutil.rmtree(path)  # removes all the subdirectories!
                os.makedirs(path)
            except:
                print("An Error Occurred")



    def calculate_minimum_r(self):
        vectors = {2: self.vector_2, 3: self.vector_3, 4: self.vector_4, 5: self.vector_5, 6: self.vector_6}
        for vector in vectors.values():
            start_force_normal_magnitude = vector.start_force.get_force_magnitude() * np.abs(np.cos(np.radians(vector.angle) - vector.start_force.get_force_angle()))

            end_force_normal_magnitude = vector.end_force.get_force_magnitude() * np.abs(
                np.cos(np.radians(vector.angle) - vector.end_force.get_force_angle()))

            p = max(np.abs(start_force_normal_magnitude), np.abs(end_force_normal_magnitude))

            p_critical = p / self.safety_factor
            r = ((p_critical * vector.length**2 * 4) / ((np.pi)**3 * vector.module_of_elasticity))**(1/4)
            sr = vector.length / (r/2)

            if sr > vector.sr_d and r > vector.minimum_r:
                vector.minimum_r = r
            elif sr < vector.sr_d:
                x = Symbol("x")
                eqn = Eq(p_critical / (np.pi * x**2) - vector.compressive_yield_strength + (1/vector.module_of_elasticity)*(vector.compressive_yield_strength * (2 * vector.length/x) / (2*np.pi))**2 , sr)
                r = solve(eqn)
                if r > vector.minimum_r:
                    vector.minimum_r = r




    def calculate_angular_properties(self):
        """
        calculate angles for six link mechanism.
        :return: angles of moving links are returned as a np.ndarray. column order : vector_2.angle, vector_3.angle,
                vector_4.angle,vector_5.angle, vector_6.angle
                ********* returned angles are in degrees! ********
        """
        initial_guess_loop_1, initial_guess_loop_2 = self.initial_guesses
        test_variable = 0

        for i in range(0, self.num_of_repeats):
            known_vectors_loop_1 = self.vector_2, self.vector_1
            unknown_vectors_loop_1 = self.vector_3, self.vector_4

            # at first we solve loop 1 which consist of vector1,vector2,vector3 and vector 4

            solver_loop_1 = FourLinkSolver(known_vectors=known_vectors_loop_1, unknown_vectors=unknown_vectors_loop_1,
                                           initial_guess=initial_guess_loop_1)
            self.vector_3.angle, self.vector_4.angle = solver_loop_1.calculate_theta()
            self.vector_3.angular_velocity, self.vector_4.angular_velocity = solver_loop_1.calculate_angular_velocity()
            self.vector_3.angular_acceleration, self.vector_4.angular_acceleration = solver_loop_1.calculate_angular_acceleration()
            # next initial guess is the last calculated theta
            initial_guess_loop_1 = np.array([self.vector_3.angle, self.vector_4.angle])

            self.vector_4_prime.angle = self.vector_4.angle
            self.vector_4_prime.angular_velocity = self.vector_4.angular_velocity
            self.vector_4_prime.angular_acceleration = self.vector_4.angular_acceleration
            known_vectors_loop_2 = self.vector_4_prime, self.vector_1_prime
            unknown_vectors_loop_2 = self.vector_5, self.vector_6

            # and then we solve loop 2 which consist of vector4_prime (has same angle of
            # vector4 with different length ,vector2,vector3 and vector 4

            solver_loop_2 = FourLinkSolver(known_vectors=known_vectors_loop_2, unknown_vectors=unknown_vectors_loop_2,
                                           initial_guess=initial_guess_loop_2)
            self.vector_5.angle, self.vector_6.angle = solver_loop_2.calculate_theta()
            self.vector_5.angular_velocity, self.vector_6.angular_velocity = solver_loop_2.calculate_angular_velocity()
            self.vector_5.angular_acceleration, self.vector_6.angular_acceleration = solver_loop_2.calculate_angular_acceleration()

            self.vector_2.theta_prime = 1
            self.vector_2.theta_zegond = 1

            initial_guess_loop_2 = np.array([self.vector_5.angle, self.vector_6.angle])

            # ################################## P and Z solver #####################################################
            if self.p_velocity_matrix[i - 1, 0] > 0:
                test_variable = 1
            elif self.p_velocity_matrix[i - 1, 0] < 0:
                test_variable = -1
            # for p r=2

            [self.p_coordinates_matrix[i, 0], self.p_coordinates_matrix[i, 1]] = self.calculate_p_z_properties(2)[0]
            self.point_p.x_coordinate, self.point_p.y_coordinate = self.p_coordinates_matrix[i, 0], \
                                                                   self.p_coordinates_matrix[i, 1]
            [self.p_velocity_matrix[i, 0], self.p_velocity_matrix[i, 1]] = self.calculate_p_z_properties(2)[1]
            self.point_p.x_velocity, self.point_p.y_velocity = self.p_velocity_matrix[i, 0], self.p_velocity_matrix[
                i, 1]
            [self.p_acceleration_matrix[i, 0], self.p_acceleration_matrix[i, 1]] = self.calculate_p_z_properties(2)[2]
            self.point_p.x_acceleration, self.point_p.y_acceleration = self.p_acceleration_matrix[i, 0], \
                                                                       self.p_acceleration_matrix[i, 1]
            [self.p_prime_matrix[i, 0], self.p_prime_matrix[i, 1]] = self.calculate_p_z_properties(2)[3]
            self.point_p.x_prime, self.point_p.y_prime = self.p_prime_matrix[i, 0], self.p_prime_matrix[i, 1]
            [self.p_zegond_matrix[i, 0], self.p_zegond_matrix[i, 1]] = self.calculate_p_z_properties(2)[4]
            self.point_p.x_double_prime, self.point_p.y_double_prime = self.p_zegond_matrix[i, 0], self.p_zegond_matrix[
                i, 1]
            self.p_center_of_curvature_matrix[i, 0], self.p_center_of_curvature_matrix[i, 1], \
            self.p_radius_of_curvature_matrix[i, 0] = self.calculate_curvature_center(self.p_coordinates_matrix[i, 0],
                                                                                      self.p_coordinates_matrix[i, 1],
                                                                                      self.p_velocity_matrix[i, 0],
                                                                                      self.p_velocity_matrix[i, 1],
                                                                                      self.p_acceleration_matrix[i, 0],
                                                                                      self.p_acceleration_matrix[i, 1],
                                                                                      test_variable)
            [self.p_tangential_vector_matrix[i, 0],
             self.p_tangential_vector_matrix[i, 1]] = \
                self.calculate_tangential_normal_vectors(self.p_velocity_matrix[i, 0], self.p_velocity_matrix[i, 1])[0]
            [self.p_normal_vector_matrix[i, 0], self.p_normal_vector_matrix[i, 1]] = \
                self.calculate_tangential_normal_vectors(self.p_velocity_matrix[i, 0], self.p_velocity_matrix[i, 1])[1]

            if self.z_velocity_matrix[i - 1, 0] > 0:
                test_variable = 1
            elif self.z_velocity_matrix[i - 1, 0] < 0:
                test_variable = -1
            # for z r=4/3
            [self.z_coordinates_matrix[i, 0], self.z_coordinates_matrix[i, 1]] = self.calculate_p_z_properties(4 / 3)[0]
            [self.z_velocity_matrix[i, 0], self.z_velocity_matrix[i, 1]] = self.calculate_p_z_properties(4 / 3)[1]
            [self.z_acceleration_matrix[i, 0], self.z_acceleration_matrix[i, 1]] = self.calculate_p_z_properties(4 / 3)[
                2]
            [self.z_prime_matrix[i, 0], self.z_prime_matrix[i, 1]] = self.calculate_p_z_properties(4 / 3)[3]
            [self.z_zegond_matrix[i, 0], self.z_zegond_matrix[i, 1]] = self.calculate_p_z_properties(4 / 3)[4]

            self.z_center_of_curvature_matrix[i, 0], self.z_center_of_curvature_matrix[i, 1], \
            self.z_radius_of_curvature_matrix[i, 0] = self.calculate_curvature_center(self.z_coordinates_matrix[i, 0],
                                                                                      self.z_coordinates_matrix[i, 1],
                                                                                      self.z_velocity_matrix[i, 0],
                                                                                      self.z_velocity_matrix[i, 1],
                                                                                      self.z_acceleration_matrix[
                                                                                          i, 0],
                                                                                      self.z_acceleration_matrix[
                                                                                          i, 1], test_variable)
            [self.z_tangential_vector_matrix[i, 0],
             self.z_tangential_vector_matrix[i, 1]] = \
                self.calculate_tangential_normal_vectors(self.z_velocity_matrix[i, 0], self.z_velocity_matrix[i, 1])[0]
            [self.z_normal_vector_matrix[i, 0], self.z_normal_vector_matrix[i, 1]] = \
                self.calculate_tangential_normal_vectors(self.z_velocity_matrix[i, 0], self.z_velocity_matrix[i, 1])[1]

            # theta prime / theta zegond / angle of each vector / angular velocity of each vector #####################
            # angular acceleration for each vector   ########################
            self.theta_prime_matrix[i, 0] = 1
            self.theta_prime_matrix[i, 1] = self.vector_3.theta_prime
            self.theta_prime_matrix[i, 2] = self.vector_4.theta_prime
            self.theta_prime_matrix[i, 3] = \
                self.convert_omega_alpha_5(self.vector_5.angular_velocity, self.vector_5.angular_acceleration)[0]
            self.theta_prime_matrix[i, 4] = \
                self.convert_omega_alpha_6(self.vector_6.angular_velocity, self.vector_6.angular_acceleration)[0]

            #   ****************important *************
            # after this section, all theta prime and all theta zegonds are based on 2
            #   ****************important *************

            self.theta_zegond_matrix[i, 0] = 0
            self.theta_zegond_matrix[i, 1] = self.vector_3.theta_zegond
            self.theta_zegond_matrix[i, 2] = self.vector_4.theta_zegond
            self.theta_zegond_matrix[i, 3] = \
                self.convert_omega_alpha_5(self.vector_5.angular_velocity, self.vector_5.angular_acceleration)[1]
            self.theta_zegond_matrix[i, 4] = \
                self.convert_omega_alpha_6(self.vector_6.angular_velocity, self.vector_6.angular_acceleration)[1]

            self.angle_matrix[i, 0] = self.vector_2.angle
            self.angle_matrix[i, 1] = self.vector_3.angle
            self.angle_matrix[i, 2] = self.vector_4.angle
            self.angle_matrix[i, 3] = self.vector_5.angle
            self.angle_matrix[i, 4] = self.vector_6.angle

            self.angular_velocity_matrix[i, 0] = self.vector_2.angular_velocity
            self.angular_velocity_matrix[i, 1] = self.vector_3.angular_velocity
            self.angular_velocity_matrix[i, 2] = self.vector_4.angular_velocity
            self.angular_velocity_matrix[i, 3] = self.vector_5.angular_velocity
            self.angular_velocity_matrix[i, 4] = self.vector_6.angular_velocity

            self.angular_acceleration_matrix[i, 0] = self.vector_2.angular_acceleration
            self.angular_acceleration_matrix[i, 1] = self.vector_3.angular_acceleration
            self.angular_acceleration_matrix[i, 2] = self.vector_4.angular_acceleration
            self.angular_acceleration_matrix[i, 3] = self.vector_5.angular_acceleration
            self.angular_acceleration_matrix[i, 4] = self.vector_6.angular_acceleration
            """
            calculate determinant of coefficients matrix
            """
            self.matrix_det_of_coefficients[i, 0] = np.linalg.det(np.array([[-self.vector_3.length * np.sin(
                np.radians(self.vector_3.angle)), -self.vector_4.length * np.sin(np.radians(self.vector_4.angle))], [
                                                                                self.vector_3.length * np.cos(
                                                                                    np.radians(self.vector_3.angle)),
                                                                                self.vector_4.length * np.cos(
                                                                                    np.radians(self.vector_4.angle))]]))
            self.matrix_det_of_coefficients[i, 1] = np.linalg.det(np.array([[-self.vector_5.length * np.sin(
                np.radians(self.vector_5.angle)), -self.vector_6.length * np.sin(np.radians(self.vector_6.angle))], [
                                                                                self.vector_5.length * np.cos(
                                                                                    np.radians(self.vector_5.angle)),
                                                                                self.vector_6.length * np.cos(
                                                                                    np.radians(self.vector_6.angle))]]))
            if self.matrix_det_of_coefficients[i, 0] == 0 or self.matrix_det_of_coefficients[i, 1] == 0:
                print(i)
            """
            dynamic part 
            """
            self.calculate_cg_acceleration()
            self.vector_3_cg_acceleration_matrix[i,0] = self.vector_3.cg.x_acceleration
            self.vector_3_cg_acceleration_matrix[i, 1] = self.vector_3.cg.y_acceleration

            known_vectors = self.vector_1, self.vector_1_prime, self.vector_2
            unknown_vectors = self.vector_3, self.vector_4, self.vector_4_prime, self.vector_5, self.vector_6

            dynamic_solver = DynamicSolver(known_vectors=known_vectors, unknown_vectors=unknown_vectors,
                                           iteration_number=i, spring=self.spring, damper=self.damper)
            dynamic_solver.spring_damper_force_calculator()
            dynamic_solver.force_calculator()
            self.calculate_minimum_r()

            for j in range(0, 15):
                self.dynamic_method_forces_matrix[i, j] = dynamic_solver.dynamic_forces_results_matrix[j, 0]


            if i % self.export_step / self.steps == 0:
                self.export_excel_forces(i, row_number=self.row_number_newton_excel, writer=self.writer_for_newton_method)
                self.row_number_newton_excel += 1
            """
            Static solver (where alphas and omegas are zero)
            """
            static_solver = StaticSolver(known_vectors=known_vectors, unknown_vectors=unknown_vectors,
                                         iteration_number=i, spring=self.spring, damper=self.damper)
            static_solver.spring_damper_force_calculator()
            static_solver.force_calculator()
            for j in range(0, 15):
                self.static_method_forces_matrix[i, j] = static_solver.static_forces_results_matrix[j, 0]

            if i % self.export_step / self.steps == 0:
                self.export_excel_forces(i, row_number=self.row_number_static_excel, writer=self.writer_for_static)
                self.row_number_static_excel += 1

            """ 
            Dynamic Solver with power method
            """

            energy_solver = EnergySolver(known_vectors=known_vectors, unknown_vectors=unknown_vectors,
                                         iteration_number=i, spring=self.spring, damper=self.damper)
            energy_solver.calculate_momentum()
            self.energy_calculated_momentum[i, 0] = energy_solver.momentum
            self.equivalent_inertia_matrix[i, 0] = energy_solver.equivalent_inertia
            self.sigma_b_matrix[i, 0] = energy_solver.sigma_b
            self.sigma_a_energy_term_matrix[i, 0] = energy_solver.sigma_a_energy_term
            self.sigma_b_energy_term_matrix[i, 0] = energy_solver.sigma_b_energy_term
            self.energy_method_spring_term_matrix[i, 0] = energy_solver.spring_term
            self.energy_method_damper_term_matrix[i, 0] = energy_solver.damper_term

            self.sigma_potential_term_matrix[i,0] = energy_solver.sigma_potential_term

            if i % self.export_step / self.steps == 0:
                self.export_energy_method_excels(energy_solver)
                self.row_number_energy_solver += 1

            # ***************************************************************************************
            # add steps to vector2.angle and also updates angular velocities and angular acceleration
            # ***************************************************************************************
            self.vector_2.update_theta(self.vector_2.angle + self.steps)
            QtWidgets.QApplication.processEvents()

    def export_energy_method_excels(self, energy_solver):
        data_frame_equivalent_inertia = DataFrame(
            [[float(self.vector_2.angle), float(energy_solver.equivalent_inertia), float(energy_solver.sigma_a_energy_term)]])
        data_frame_equivalent_inertia.to_excel(self.writer_for_energy,
                                               sheet_name=self.excel_sheet_names_energy_method[0], header=None,
                                               index=None, startrow=self.row_number_energy_solver)
        data_frame_equivalent_inertia = DataFrame(
            [[float(self.vector_2.angle), float(energy_solver.sigma_b), float(energy_solver.sigma_b_energy_term)]])
        data_frame_equivalent_inertia.to_excel(self.writer_for_energy,
                                               sheet_name=self.excel_sheet_names_energy_method[1], header=None,
                                               index=None, startrow=self.row_number_energy_solver)


        data_frame_equivalent_inertia = DataFrame([[float(self.vector_2.angle), float(energy_solver.momentum)]])
        data_frame_equivalent_inertia.to_excel(self.writer_for_energy,
                                               sheet_name=self.excel_sheet_names_energy_method[2], header=None,
                                               index=None, startrow=self.row_number_energy_solver)

    def export_excel_forces(self, i, writer, row_number):
        writer = writer
        row_number = row_number
        vectors_to_export = {0: self.vector_2, 1: self.vector_3, 2: self.vector_4, 3: self.vector_5,
                             4: self.vector_6}

        for vector_index in range(0, 5):
            data_frame = DataFrame([[float(self.vector_2.angle),
                                     float(vectors_to_export[vector_index].start_force.x_force),
                                     float(vectors_to_export[vector_index].start_force.y_force),
                                     float(vectors_to_export[vector_index].end_force.x_force),
                                     float(vectors_to_export[vector_index].end_force.y_force)]])
            data_frame.to_excel(writer,
                                sheet_name=self.excel_sheet_names_of_forces_dynamic[vector_index], header=None,
                                index=None, startrow=row_number)

        data_frame_spring = DataFrame([[self.vector_2.angle, self.spring.force]])
        data_frame_spring.to_excel(writer,
                            sheet_name=self.excel_sheet_names_of_forces_dynamic[5], header=None,
                            index=None, startrow=row_number)

        data_frame_damper = DataFrame([[self.vector_2.angle, self.damper.force]])
        data_frame_damper.to_excel(writer,
                            sheet_name=self.excel_sheet_names_of_forces_dynamic[6], header=None,
                            index=None, startrow=row_number)

        data_frame_momentum = DataFrame([[self.vector_2.angle, self.vector_2.momentum]])
        data_frame_momentum.to_excel(writer,
                            sheet_name=self.excel_sheet_names_of_forces_dynamic[7], header=None,
                            index=None, startrow=row_number)


    def calculate_p_z_properties(self, r):
        """coordinates_matrix = np.zeros((self.num_of_repeats, 2))
        linear_velocity_matrix = np.zeros((self.num_of_repeats, 2))
        linear_acceleration_matrix = np.zeros((self.num_of_repeats, 2))
        primes_on_2_matrix = np.zeros((self.num_of_repeats, 2))
        zegonds_on_2_matrix = np.zeros((self.num_of_repeats, 2))"""

        x_coordinates = -(self.vector_5.length / r * np.cos(
            np.radians(self.vector_5.angle)) + self.vector_4_prime.length * np.cos(np.radians(self.vector_4.angle))) - (
                                self.vector_1.length * np.cos(np.radians(self.vector_1.angle)))
        y_coordinates = -(self.vector_5.length / r * np.sin(
            np.radians(self.vector_5.angle)) + self.vector_4_prime.length * np.sin(np.radians(self.vector_4.angle))) - (
                                self.vector_1.length * np.sin(np.radians(self.vector_1.angle)))

        x_prime = self.vector_5.length / r * np.sin(
            np.radians(self.vector_5.angle)) * self.vector_5.theta_prime + self.vector_4_prime.length * np.sin(
            np.radians(self.vector_4.angle))
        y_prime = -(self.vector_5.length / r * np.cos(
            np.radians(self.vector_5.angle)) * self.vector_5.theta_prime + self.vector_4_prime.length * np.cos(
            np.radians(self.vector_4.angle)))

        x_velocity = x_prime * self.vector_4.angular_velocity
        y_velocity = y_prime * self.vector_4.angular_velocity

        x_zegond = self.vector_5.length / r * self.vector_5.theta_zegond * np.sin(
            np.radians(self.vector_5.angle)) + self.vector_5.length / r * self.vector_5.theta_prime ** 2 * np.cos(
            np.radians(self.vector_5.angle)) + self.vector_4_prime.length * np.cos(np.radians(self.vector_4.angle))
        y_zegond = -self.vector_5.length / r * self.vector_5.theta_zegond * np.cos(
            np.radians(self.vector_5.angle)) + self.vector_5.length / r * self.vector_5.theta_prime ** 2 * np.sin(
            np.radians(self.vector_5.angle)) + self.vector_4_prime.length * np.sin(np.radians(self.vector_4.angle))

        x_acceleration = x_zegond * (self.vector_4.angular_velocity ** 2) + x_prime * self.vector_4.angular_acceleration
        y_acceleration = y_zegond * (self.vector_4.angular_velocity ** 2) + y_prime * self.vector_4.angular_acceleration

        coordinates = [x_coordinates, y_coordinates]

        velocity = [x_velocity, y_velocity]

        acceleration = [x_acceleration, y_acceleration]
        if self.vector_2.angular_velocity == 0:
            primes_on_2 = [x_prime * self.vector_4.theta_prime, y_prime * self.vector_4.theta_prime]
            zegonds_on_2 = [x_zegond * self.vector_4.theta_prime ** 2 + x_prime * self.vector_4.theta_zegond,
                            y_zegond * self.vector_4.theta_prime ** 2 + y_prime * self.vector_4.theta_zegond]
        else:
            primes_on_2 = [x_velocity / self.vector_2.angular_velocity, y_velocity / self.vector_2.angular_velocity]
            zegonds_on_2 = [(x_acceleration - (
                    x_velocity / self.vector_2.angular_velocity) * self.vector_2.angular_acceleration) / self.vector_2.angular_velocity ** 2,
                            (y_acceleration - (
                                    y_velocity / self.vector_2.angular_velocity) * self.vector_2.angular_acceleration) / self.vector_2.angular_velocity ** 2]

        return coordinates, velocity, acceleration, primes_on_2, zegonds_on_2

    def calculate_p_z_distance(self, coordinates_matrix):
        r = 0
        for i in range(0, self.num_of_repeats - 1):
            r = r + np.sqrt((coordinates_matrix[i, 0] - coordinates_matrix[i + 1, 0]) ** 2 + (
                    coordinates_matrix[i, 1] - coordinates_matrix[i + 1, 1]) ** 2)
        return r

    def convert_omega_alpha_5(self, omega, alpha):
        if self.vector_2.angular_velocity == 0:
            theta_prime_base_on_two = self.vector_5.theta_prime * self.vector_4.theta_prime
            theta_zegond_base_on_two = self.vector_5.theta_zegond * self.vector_4.theta_prime ** 2 + self.vector_5.theta_prime * self.vector_4.theta_zegond
        else:
            theta_prime_base_on_two = omega / self.vector_2.angular_velocity
            theta_zegond_base_on_two = (alpha - (
                    omega / self.vector_2.angular_velocity * self.vector_2.angular_acceleration)) / self.vector_2.angular_velocity ** 2
        self.vector_5.theta_prime = theta_prime_base_on_two
        self.vector_5.theta_zegond = theta_zegond_base_on_two
        return theta_prime_base_on_two, theta_zegond_base_on_two

    def convert_omega_alpha_6(self, omega, alpha):
        if self.vector_2.angular_velocity == 0:
            theta_prime_base_on_two = self.vector_6.theta_prime * self.vector_4.theta_prime
            theta_zegond_base_on_two = self.vector_6.theta_zegond * self.vector_4.theta_prime ** 2 + self.vector_6.theta_prime * self.vector_4.theta_zegond
        else:
            theta_prime_base_on_two = omega / self.vector_2.angular_velocity
            theta_zegond_base_on_two = (alpha - (
                    omega / self.vector_2.angular_velocity * self.vector_2.angular_acceleration)) / self.vector_2.angular_velocity ** 2

        self.vector_6.theta_prime = theta_prime_base_on_two
        self.vector_6.theta_zegond = theta_zegond_base_on_two
        return theta_prime_base_on_two, theta_zegond_base_on_two

    def calculate_curvature_center(self, x, y, v_x, v_y, a_x, a_y, test_variable):
        # define new method to solve curvature problem
        if v_x == 0 and v_y >= 0 and test_variable == 1:
            theta = math.pi / 2
        elif v_x == 0 and v_y < 0 and test_variable == 1:
            theta = -math.pi / 2
        elif v_x == 0 and v_y > 0 and test_variable == -1:
            theta = -math.pi / 2
        elif v_x == 0 and v_y < 0 and test_variable == -1:
            theta = math.pi / 2
        elif v_x == v_y == 0:
            theta = 0
        else:
            theta = np.arctan(v_y / v_x)
        r = a_y * np.cos(theta) - a_x * np.sin(theta)
        a_n_vector = array([-r * np.sin(theta), r * np.cos(theta)])
        norm_a_n_vector = la.norm(a_n_vector)
        a_vector = array([a_x, a_y])
        v_vector = array([v_x, v_y])
        if la.norm(a_n_vector) == 0:
            radius_of_curvature = math.inf
            curvature_vector = array([math.inf, math.inf])
            x_center_of_curvature = curvature_vector[0]
            y_center_of_curvature = curvature_vector[1]
        elif la.norm(v_vector) == 0 or (la.norm(np.cross(v_vector, a_vector)) / la.norm(v_vector) ** 3) == 0:
            radius_of_curvature = None
            curvature_vector = array([None, None])
            x_center_of_curvature = curvature_vector[0]
            y_center_of_curvature = curvature_vector[1]
        else:
            radius_of_curvature = (la.norm(np.cross(v_vector, a_vector)) / la.norm(v_vector) ** 3) ** (-1)
            curvature_vector = (radius_of_curvature / norm_a_n_vector) * a_n_vector
            x_center_of_curvature = curvature_vector[0] + x
            y_center_of_curvature = curvature_vector[1] + y
        return x_center_of_curvature, y_center_of_curvature, radius_of_curvature

    def calculate_tangential_normal_vectors(self, v_x, v_y):
        r = np.sqrt(v_x ** 2 + v_y ** 2)
        tangential_vector = [v_x / r, v_y / r]
        normal_vector = [-v_y / r, v_x / r]
        return tangential_vector, normal_vector

    def calculate_cg_acceleration(self):
        self.calculate_cg_properties_of_link_3()
        self.vector_5.cg = self.point_p
        # print("alpha 2 = ", self.vector_2.angle, "cg 3 vx= ", self.vector_3.cg.x_velocity, "cg 5 vx= ", self.vector_5.cg.x_velocity)

    def calculate_cg_properties_of_link_3(self):
        self.vector_3.cg.x_prime = - self.vector_2.length * np.sin(
            np.radians(self.vector_2.angle)) - self.vector_3.length / 2 * self.vector_3.theta_prime * np.sin(
            np.radians(self.vector_3.angle))
        self.vector_3.cg.y_prime = + self.vector_2.length * np.cos(
            np.radians(self.vector_2.angle)) + self.vector_3.length / 2 * self.vector_3.theta_prime * np.cos(
            np.radians(self.vector_3.angle))

        self.vector_3.cg.x_double_prime = - self.vector_2.length * np.cos(
            np.radians(self.vector_2.angle)) - self.vector_3.length / 2 * (self.vector_3.theta_prime ** 2) * np.cos(
            np.radians(self.vector_3.angle)) - self.vector_3.length / 2 * self.vector_3.theta_zegond * np.sin(
            np.radians(self.vector_3.angle))
        self.vector_3.cg.y_double_prime = - self.vector_2.length * np.sin(
            np.radians(self.vector_2.angle)) - self.vector_3.length / 2 * (self.vector_3.theta_prime ** 2) * np.sin(
            np.radians(self.vector_3.angle)) + self.vector_3.length / 2 * self.vector_3.theta_zegond * np.cos(
            np.radians(self.vector_3.angle))

        self.vector_3.cg.x_acceleration = (
                                                  self.vector_2.angular_velocity ** 2) * self.vector_3.cg.x_double_prime + self.vector_2.angular_acceleration * self.vector_3.cg.x_prime
        self.vector_3.cg.y_acceleration = (
                                                  self.vector_2.angular_velocity ** 2) * self.vector_3.cg.y_double_prime + self.vector_2.angular_acceleration * self.vector_3.cg.y_prime




class DynamicSolver:
    def __init__(self, known_vectors: Tuple[KnownVector, KnownVector, KnownVector],
                 unknown_vectors: Tuple[UnKnownVector, UnKnownVector, UnKnownVector, UnKnownVector, UnKnownVector],
                 iteration_number: int, spring: Spring, damper: Damper):
        """
        inputs must be in a shape like this:
        :param known_vectors Tuple[vector_1, vector_1_prime, vector_2] which are KnownVector objects
        :param unknown_vectors Tuple[vector_3, vector_4,vector_4_prime vector_5, vector_6] which are UnKnownVector objects
        :param loop_number int
        vector 1 (earth) (O2 - O4)
        vector 1 prime (earth) (O6-O4)
        """
        self.vector_1, self.vector_1_prime, self.vector_2 = known_vectors
        self.vector_3, self.vector_4, self.vector_4_prime, self.vector_5, self.vector_6 = unknown_vectors
        self.iteration_number = iteration_number

        self.force_coefficient_matrix = np.zeros((15, 15))
        self.force_constant_matrix = np.zeros((15, 1))
        self.dynamic_forces_results_matrix = np.zeros((15, 1))
        self.force_dict = {}
        self.spring = spring
        self.damper = damper

        self.spring_angle = None

    def spring_damper_force_calculator(self):
        """
         this method calculate damper and spring force in each loop
        """

        self.damper.force = -self.vector_5.cg.x_velocity * self.damper.damping_coefficient
        self.spring.force = self.spring.k * (
                -np.sqrt(
                    self.vector_5.cg.x_coordinate ** 2 + self.vector_5.cg.y_coordinate ** 2) + self.spring.free_length)
        self.spring_angle = np.arctan(self.vector_5.cg.x_coordinate / self.vector_5.cg.y_coordinate)

    def force_calculator(self):
        g = 9.81
        self.force_coefficient_matrix[0, 1] = 1
        self.force_coefficient_matrix[0, 3] = 1
        self.force_coefficient_matrix[1, 0] = 1
        self.force_coefficient_matrix[1, 2] = 1
        self.force_coefficient_matrix[2, 2] = +self.vector_2.length * np.sin(np.radians(self.vector_2.angle))
        self.force_coefficient_matrix[2, 3] = -self.vector_2.length * np.cos(np.radians(self.vector_2.angle))
        self.force_coefficient_matrix[2, 14] = 1
        self.force_coefficient_matrix[3, 2] = 1
        self.force_coefficient_matrix[3, 4] = 1
        self.force_coefficient_matrix[4, 3] = 1
        self.force_coefficient_matrix[4, 5] = 1
        self.force_coefficient_matrix[5, 2] = -self.vector_3.length / 2 * np.sin(np.radians(self.vector_3.angle))
        self.force_coefficient_matrix[5, 3] = +self.vector_3.length / 2 * np.cos(np.radians(self.vector_3.angle))
        self.force_coefficient_matrix[5, 4] = +self.vector_3.length / 2 * np.sin(np.radians(self.vector_3.angle))
        self.force_coefficient_matrix[5, 5] = -self.vector_3.length / 2 * np.cos(np.radians(self.vector_3.angle))
        self.force_coefficient_matrix[6, 4] = 1
        self.force_coefficient_matrix[6, 6] = 1
        self.force_coefficient_matrix[6, 8] = 1
        self.force_coefficient_matrix[7, 5] = 1
        self.force_coefficient_matrix[7, 7] = 1
        self.force_coefficient_matrix[7, 9] = 1
        self.force_coefficient_matrix[8, 4] = -self.vector_4.length * np.sin(np.radians(self.vector_4.angle))
        self.force_coefficient_matrix[8, 5] = +self.vector_4.length * np.cos(np.radians(self.vector_4.angle))
        self.force_coefficient_matrix[8, 6] = -self.vector_4_prime.length * np.sin(np.radians(self.vector_4.angle))
        self.force_coefficient_matrix[8, 7] = +self.vector_4_prime.length * np.cos(np.radians(self.vector_4.angle))
        self.force_coefficient_matrix[9, 6] = 1
        self.force_coefficient_matrix[9, 10] = 1
        self.force_coefficient_matrix[10, 7] = 1
        self.force_coefficient_matrix[10, 11] = 1
        self.force_coefficient_matrix[11, 6] = +self.vector_5.length / 2 * np.sin(
            np.radians(self.vector_5.angle))
        self.force_coefficient_matrix[11, 7] = -self.vector_5.length / 2 * np.cos(
            np.radians(self.vector_5.angle))
        self.force_coefficient_matrix[11, 10] = -self.vector_5.length / 2 * np.sin(
            np.radians(self.vector_5.angle))
        self.force_coefficient_matrix[11, 11] = +self.vector_5.length / 2 * np.cos(
            np.radians(self.vector_5.angle))
        self.force_coefficient_matrix[12, 10] = 1
        self.force_coefficient_matrix[12, 12] = 1
        self.force_coefficient_matrix[13, 11] = 1
        self.force_coefficient_matrix[13, 13] = 1
        self.force_coefficient_matrix[14, 10] = +self.vector_6.length * np.sin(np.radians(self.vector_6.angle))
        self.force_coefficient_matrix[14, 11] = -self.vector_6.length * np.cos(np.radians(self.vector_6.angle))

        self.force_constant_matrix[0, 0] = self.vector_2.mass * g
        self.force_constant_matrix[2, 0] = self.vector_2.inertia * self.vector_2.angular_acceleration
        self.force_constant_matrix[3, 0] = self.vector_3.mass * self.vector_3.cg.x_acceleration
        self.force_constant_matrix[4, 0] = self.vector_3.mass * g + self.vector_3.mass * self.vector_3.cg.y_acceleration
        self.force_constant_matrix[5, 0] = self.vector_3.inertia * self.vector_3.angular_acceleration
        self.force_constant_matrix[7, 0] = self.vector_4.mass * g
        self.force_constant_matrix[8, 0] = self.vector_4.inertia * self.vector_4.angular_acceleration
        self.force_constant_matrix[9, 0] = -self.damper.force - self.spring.force * np.sin(
            self.spring_angle) + self.vector_5.mass * self.vector_5.cg.x_acceleration
        self.force_constant_matrix[10, 0] = -self.spring.force * np.cos(
            self.spring_angle) + self.vector_5.mass * self.vector_5.cg.y_acceleration + self.vector_5.mass * g
        self.force_constant_matrix[11, 0] = self.vector_5.inertia * self.vector_5.angular_acceleration
        self.force_constant_matrix[13, 0] = self.vector_6.mass * g
        self.force_constant_matrix[14, 0] = self.vector_6.inertia * self.vector_6.angular_acceleration

        self.dynamic_forces_results_matrix = np.linalg.solve(self.force_coefficient_matrix, self.force_constant_matrix)

        self.vector_2.start_force.x_force = float(self.dynamic_forces_results_matrix[0])
        self.vector_2.start_force.y_force = float(self.dynamic_forces_results_matrix[1])
        self.vector_2.end_force.x_force = - float(self.dynamic_forces_results_matrix[2])
        self.vector_2.end_force.y_force = - float(self.dynamic_forces_results_matrix[3])

        self.vector_3.start_force.x_force = float(self.dynamic_forces_results_matrix[2])
        self.vector_3.start_force.y_force = float(self.dynamic_forces_results_matrix[3])
        self.vector_3.end_force.x_force = - float(self.dynamic_forces_results_matrix[4])
        self.vector_3.end_force.y_force = - float(self.dynamic_forces_results_matrix[5])

        self.vector_4.start_force.x_force = float(self.dynamic_forces_results_matrix[4])
        self.vector_4.start_force.y_force = float(self.dynamic_forces_results_matrix[5])
        self.vector_4.end_force.x_force = float(self.dynamic_forces_results_matrix[8])
        self.vector_4.end_force.y_force = float(self.dynamic_forces_results_matrix[9])

        self.vector_5.start_force.x_force = - float(self.dynamic_forces_results_matrix[10])
        self.vector_5.start_force.y_force = - float(self.dynamic_forces_results_matrix[11])
        self.vector_5.end_force.x_force = float(self.dynamic_forces_results_matrix[6])
        self.vector_5.end_force.y_force = float(self.dynamic_forces_results_matrix[7])

        self.vector_6.start_force.x_force = float(self.dynamic_forces_results_matrix[12])
        self.vector_6.start_force.y_force = float(self.dynamic_forces_results_matrix[13])
        self.vector_6.end_force.x_force = float(self.dynamic_forces_results_matrix[10])
        self.vector_6.end_force.y_force = float(self.dynamic_forces_results_matrix[11])



        self.vector_2.momentum = float(self.dynamic_forces_results_matrix[14])


class StaticSolver:
    def __init__(self, known_vectors: Tuple[KnownVector, KnownVector, KnownVector],
                 unknown_vectors: Tuple[UnKnownVector, UnKnownVector, UnKnownVector, UnKnownVector, UnKnownVector],
                 iteration_number: int, spring: Spring, damper: Damper):
        """
        inputs must be in a shape like this:
        :param known_vectors Tuple[vector_1, vector_1_prime, vector_2] which are KnownVector objects
        :param unknown_vectors Tuple[vector_3, vector_4,vector_4_prime vector_5, vector_6] which are UnKnownVector objects
        :param loop_number int
        vector 1 (earth) (O2 - O4)
        vector 1 prime (earth) (O6-O4)
        """
        self.vector_1, self.vector_1_prime, self.vector_2 = known_vectors
        self.vector_3, self.vector_4, self.vector_4_prime, self.vector_5, self.vector_6 = unknown_vectors
        self.iteration_number = iteration_number

        self.static_force_coefficient_matrix = np.zeros((15, 15))
        self.static_force_constant_matrix = np.zeros((15, 1))
        self.static_forces_results_matrix = np.zeros((15, 1))
        self.spring = spring
        self.damper = damper
        self.spring_angle = None

    def spring_damper_force_calculator(self):
        """
         this method calculate damper and spring force in each loop
        """

        self.damper.force = 0
        self.spring.force = self.spring.k * (
                -np.sqrt(
                    self.vector_5.cg.x_coordinate ** 2 + self.vector_5.cg.y_coordinate ** 2) + self.spring.free_length)
        self.spring_angle = np.arctan(self.vector_5.cg.x_coordinate / self.vector_5.cg.y_coordinate)
        print((
                -np.sqrt(
                    self.vector_5.cg.x_coordinate ** 2 + self.vector_5.cg.y_coordinate ** 2) + self.spring.free_length))

    def force_calculator(self):
        g = 9.81
        self.static_force_coefficient_matrix[0, 1] = 1
        self.static_force_coefficient_matrix[0, 3] = 1
        self.static_force_coefficient_matrix[1, 0] = 1
        self.static_force_coefficient_matrix[1, 2] = 1
        self.static_force_coefficient_matrix[2, 2] = +self.vector_2.length * np.sin(np.radians(self.vector_2.angle))
        self.static_force_coefficient_matrix[2, 3] = -self.vector_2.length * np.cos(np.radians(self.vector_2.angle))
        self.static_force_coefficient_matrix[2, 14] = 1
        self.static_force_coefficient_matrix[3, 2] = 1
        self.static_force_coefficient_matrix[3, 4] = 1
        self.static_force_coefficient_matrix[4, 3] = 1
        self.static_force_coefficient_matrix[4, 5] = 1
        self.static_force_coefficient_matrix[5, 2] = -self.vector_3.length / 2 * np.sin(np.radians(self.vector_3.angle))
        self.static_force_coefficient_matrix[5, 3] = +self.vector_3.length / 2 * np.cos(np.radians(self.vector_3.angle))
        self.static_force_coefficient_matrix[5, 4] = +self.vector_3.length / 2 * np.sin(np.radians(self.vector_3.angle))
        self.static_force_coefficient_matrix[5, 5] = -self.vector_3.length / 2 * np.cos(np.radians(self.vector_3.angle))
        self.static_force_coefficient_matrix[6, 4] = 1
        self.static_force_coefficient_matrix[6, 6] = 1
        self.static_force_coefficient_matrix[6, 8] = 1
        self.static_force_coefficient_matrix[7, 5] = 1
        self.static_force_coefficient_matrix[7, 7] = 1
        self.static_force_coefficient_matrix[7, 9] = 1
        self.static_force_coefficient_matrix[8, 4] = -self.vector_4.length * np.sin(np.radians(self.vector_4.angle))
        self.static_force_coefficient_matrix[8, 5] = +self.vector_4.length * np.cos(np.radians(self.vector_4.angle))
        self.static_force_coefficient_matrix[8, 6] = -self.vector_4_prime.length * np.sin(
            np.radians(self.vector_4.angle))
        self.static_force_coefficient_matrix[8, 7] = +self.vector_4_prime.length * np.cos(
            np.radians(self.vector_4.angle))
        self.static_force_coefficient_matrix[9, 6] = 1
        self.static_force_coefficient_matrix[9, 10] = 1
        self.static_force_coefficient_matrix[10, 7] = 1
        self.static_force_coefficient_matrix[10, 11] = 1
        self.static_force_coefficient_matrix[11, 6] = +self.vector_5.length / 2 * np.sin(
            np.radians(self.vector_5.angle))
        self.static_force_coefficient_matrix[11, 7] = -self.vector_5.length / 2 * np.cos(
            np.radians(self.vector_5.angle))
        self.static_force_coefficient_matrix[11, 10] = -self.vector_5.length / 2 * np.sin(
            np.radians(self.vector_5.angle))
        self.static_force_coefficient_matrix[11, 11] = +self.vector_5.length / 2 * np.cos(
            np.radians(self.vector_5.angle))
        self.static_force_coefficient_matrix[12, 10] = 1
        self.static_force_coefficient_matrix[12, 12] = 1
        self.static_force_coefficient_matrix[13, 11] = 1
        self.static_force_coefficient_matrix[13, 13] = 1
        self.static_force_coefficient_matrix[14, 10] = +self.vector_6.length * np.sin(np.radians(self.vector_6.angle))
        self.static_force_coefficient_matrix[14, 11] = -self.vector_6.length * np.cos(np.radians(self.vector_6.angle))

        self.static_force_constant_matrix[0, 0] = self.vector_2.mass * g
        self.static_force_constant_matrix[2, 0] = 0
        self.static_force_constant_matrix[3, 0] = 0
        self.static_force_constant_matrix[4, 0] = self.vector_3.mass * g + 0
        self.static_force_constant_matrix[5, 0] = 0
        self.static_force_constant_matrix[7, 0] = self.vector_4.mass * g
        self.static_force_constant_matrix[8, 0] = 0
        self.static_force_constant_matrix[9, 0] = -self.damper.force - self.spring.force * np.sin(
            self.spring_angle)
        self.static_force_constant_matrix[10, 0] = -self.spring.force * np.cos(
            self.spring_angle) + self.vector_5.mass * g
        self.static_force_constant_matrix[11, 0] = 0
        self.static_force_constant_matrix[13, 0] = self.vector_6.mass * g
        self.static_force_constant_matrix[14, 0] = 0

        self.static_forces_results_matrix = np.linalg.solve(self.static_force_coefficient_matrix,
                                                            self.static_force_constant_matrix)

        self.vector_2.start_force.x_force = float(self.static_forces_results_matrix[0])
        self.vector_2.start_force.y_force = float(self.static_forces_results_matrix[1])
        self.vector_2.end_force.x_force = - float(self.static_forces_results_matrix[2])
        self.vector_2.end_force.y_force = - float(self.static_forces_results_matrix[3])

        self.vector_3.start_force.x_force = float(self.static_forces_results_matrix[2])
        self.vector_3.start_force.y_force = float(self.static_forces_results_matrix[3])
        self.vector_3.end_force.x_force = - float(self.static_forces_results_matrix[4])
        self.vector_3.end_force.y_force = - float(self.static_forces_results_matrix[5])

        self.vector_4.start_force.x_force = float(self.static_forces_results_matrix[4])
        self.vector_4.start_force.y_force = float(self.static_forces_results_matrix[5])
        self.vector_4.end_force.x_force = float(self.static_forces_results_matrix[8])
        self.vector_4.end_force.y_force = float(self.static_forces_results_matrix[9])

        self.vector_5.start_force.x_force = - float(self.static_forces_results_matrix[10])
        self.vector_5.start_force.y_force = - float(self.static_forces_results_matrix[11])
        self.vector_5.end_force.x_force = float(self.static_forces_results_matrix[6])
        self.vector_5.end_force.y_force = float(self.static_forces_results_matrix[7])

        self.vector_6.start_force.x_force = float(self.static_forces_results_matrix[12])
        self.vector_6.start_force.y_force = float(self.static_forces_results_matrix[13])
        self.vector_6.end_force.x_force = float(self.static_forces_results_matrix[10])
        self.vector_6.end_force.y_force = float(self.static_forces_results_matrix[11])

        self.vector_2.momentum = float(self.static_forces_results_matrix[14])

        # print("angle", self.vector_2.angle)
        # print( "vector 4 : ", "fx start 4 : ", self.vector_4.start_force.x_force, "fy start 4: ", self.vector_4.start_force.y_force)
        # print( "vector 4 : ", "fx end 4 : ", self.vector_4.end_force.x_force, "fy start 4: ", self.vector_4.end_force.y_force)
        #
        # print( "vector 5 : ", "fx start 5 : ", self.vector_5.start_force.x_force, "fy start 5: ", self.vector_5.start_force.y_force)
        # print( "vector 5 : ", "fx end 5 : ", self.vector_5.end_force.x_force, "fy start 5: ", self.vector_5.end_force.y_force)


class EnergySolver:
    def __init__(self, known_vectors: Tuple[KnownVector, KnownVector, KnownVector],
                 unknown_vectors: Tuple[UnKnownVector, UnKnownVector, UnKnownVector, UnKnownVector, UnKnownVector],
                 iteration_number: int, spring: Spring, damper: Damper):
        """
        inputs must be in a shape like this:
        :param known_vectors Tuple[vector_1, vector_1_prime, vector_2] which are KnownVector objects
        :param unknown_vectors Tuple[vector_3, vector_4,vector_4_prime vector_5, vector_6] which are UnKnownVector objects
        :param loop_number int
        vector 1 (earth) (O2 - O4)
        vector 1 prime (earth) (O6-O4)
        """
        vector_1, vector_1_prime, vector_2 = known_vectors
        vector_3, vector_4, vector_4_prime, vector_5, vector_6 = unknown_vectors
        self.iteration_number = iteration_number
        self.vectors = {2: vector_2, 3: vector_3, 4: vector_4, 5: vector_5, 6: vector_6}
        self.equivalent_inertia = 0
        self.sigma_b = 0
        self.spring_term = 0
        self.sigma_a_energy_term = 0
        self.sigma_b_energy_term = 0
        self.damper_term = 0
        self.sigma_potential_term = 0
        self.momentum = 0
        self.g = 9.81
        self.spring = spring
        self.damper = damper

    def calculate_momentum(self):
        # A = m * ((xG')^2 +(yG')^2)+ IG *(theta')^2
        # B = m * ((xG')*(xG") + (yG')*(yG")) + IG * (theta') * (theta")

        for current_vector in self.vectors.values():
            current_vector.a = current_vector.mass * (
                        current_vector.cg.x_prime ** 2 + current_vector.cg.y_prime ** 2) + current_vector.inertia * (
                                       current_vector.theta_prime**2)
            current_vector.b = current_vector.mass * (
                    current_vector.cg.x_prime * current_vector.cg.x_double_prime + current_vector.cg.y_prime * current_vector.cg.y_double_prime) + current_vector.inertia * current_vector.theta_prime * current_vector.theta_zegond
            potential_term = current_vector.mass * self.g * current_vector.cg.y_prime

            self.sigma_potential_term += potential_term
            self.equivalent_inertia += current_vector.a
            self.sigma_b += current_vector.b
            self.sigma_b_energy_term += current_vector.b * (self.vectors[2].angular_velocity ** 2)
            self.sigma_a_energy_term += current_vector.a * self.vectors[2].angular_acceleration
            self.momentum += current_vector.a * self.vectors[2].angular_acceleration + current_vector.b * (
                        self.vectors[2].angular_velocity ** 2) + potential_term

        # adding spring term
        r_spring = np.sqrt(self.vectors[5].cg.x_coordinate ** 2 + self.vectors[5].cg.y_coordinate ** 2)
        r_spring_prime = (self.vectors[5].cg.x_coordinate * self.vectors[5].cg.x_prime + self.vectors[
            5].cg.y_coordinate * self.vectors[5].cg.y_prime) / r_spring
        self.spring_term = self.spring.k * (r_spring - self.spring.free_length) * r_spring_prime

        self.momentum += self.spring_term

        # adding damper term
        r_damper_prime = self.vectors[5].cg.x_prime
        self.damper_term = self.damper.damping_coefficient * (r_damper_prime ** 2) * self.vectors[2].angular_velocity
        self.momentum += self.damper_term

        # return self.momentum, self.equivalent_inertia
