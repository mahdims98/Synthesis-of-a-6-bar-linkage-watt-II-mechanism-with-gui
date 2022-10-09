import numpy as np
from scipy.optimize import fsolve
from typing import Tuple
from PyQt5 import QtWidgets
from numpy import array
from numpy import linalg as la
import math


class Vector:
    def __init__(self, length: float):
        """ this class represent a vector that has length and angle between vector direction and positive direction
        of x axis
        :param float length: vector length in (m)
        """
        self.length = length
        self.angle = None
        self.angular_acceleration = None
        self.angular_velocity = None
        self.theta_prime = None
        self.theta_zegond = None


class KnownVector(Vector):
    def __init__(self, length: float, angle: float):
        """ this class represent a vector that has length and angle between vector direction and positive direction
        of x axis
        :param float angle: angle in degrees, angle between vector and positive direction of vector
        :param float length: vector length in (m)
        """
        super().__init__(length)
        self.angle = angle
        self.update_theta(angle)

    def update_theta(self, new_theta):
        if new_theta > 360:
            self.angle = new_theta - 360
        else:
            self.angle = new_theta

        self.angle = np.round(self.angle, 3)

        if 0 <= self.angle < 50:
            self.angular_acceleration = -5 * np.pi
            self.angular_velocity = np.sqrt(((-5 * np.pi * self.angular_acceleration) / 9) * (1 - (self.angle / 50)))

        elif 50 <= self.angle < 150:
            self.angular_acceleration = +6 * np.pi
            self.angular_velocity = np.sqrt(((10 * np.pi * self.angular_acceleration) / 9) * ((self.angle - 50) / 100))

        elif 150 <= self.angle < 250:
            self.angular_acceleration = -6 * np.pi
            self.angular_velocity = np.sqrt(
                ((-10 * np.pi * self.angular_acceleration) / 9) * (1 - ((self.angle - 150) / 100)))

        elif 250 <= self.angle < 330:
            self.angular_acceleration = +5 * np.pi
            self.angular_velocity = np.sqrt(((8 * np.pi * self.angular_acceleration) / 9) * ((self.angle - 250) / 80))

        elif 330 <= self.angle < 360:
            self.angular_acceleration = -5 * np.pi
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
                 initial_guesses: Tuple[np.ndarray, np.ndarray], num_of_repeats: int, steps: int):
        """
        inputs must be in a shape like this:
        :param known_vectors Tuple[vector_1, vector_1_prime, vector_2] which are KnownVector objects
        :param unknown_vectors Tuple[vector_3, vector_4,vector_4_prime vector_5, vector_6] which are UnKnownVector objects
        :param initial_guesses Tuple[initial_guess_loop_1, initial_guess_loop_2] which are np.arrays objects
        :param steps : int , angle steps
        :param num_of_repeats: int, how many loops are needed?
        vector 1 (earth) (O2 - O4)
        vector 1 prime (earth) (O6-o4)
        """
        self.vector_1, self.vector_1_prime, self.vector_2 = known_vectors
        self.vector_3, self.vector_4, self.vector_4_prime, self.vector_5, self.vector_6 = unknown_vectors
        self.initial_guesses = initial_guesses
        self.steps = steps
        self.num_of_repeats = num_of_repeats

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

    def calculate_angular_properties(self) -> Tuple[np.ndarray, np.ndarray]:
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

            initial_guess_loop_2 = np.array([self.vector_5.angle, self.vector_6.angle])

            # ################################## P and Z solver #####################################################
            if self.p_velocity_matrix[i - 1, 0] > 0:
                test_variable = 1
            elif self.p_velocity_matrix[i - 1, 0] < 0:
                test_variable = -1
            # for p r=2
            [self.p_coordinates_matrix[i, 0], self.p_coordinates_matrix[i, 1]] = self.calculate_p_z_properties(2)[0]
            [self.p_velocity_matrix[i, 0], self.p_velocity_matrix[i, 1]] = self.calculate_p_z_properties(2)[1]
            [self.p_acceleration_matrix[i, 0], self.p_acceleration_matrix[i, 1]] = self.calculate_p_z_properties(2)[2]
            [self.p_prime_matrix[i, 0], self.p_prime_matrix[i, 1]] = self.calculate_p_z_properties(2)[3]
            [self.p_zegond_matrix[i, 0], self.p_zegond_matrix[i, 1]] = self.calculate_p_z_properties(2)[4]
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
            self.transfer_case_5(self.vector_5.angular_velocity, self.vector_5.angular_acceleration)[0]
            self.theta_prime_matrix[i, 4] = \
            self.transfer_case_6(self.vector_6.angular_velocity, self.vector_6.angular_acceleration)[0]

            self.theta_zegond_matrix[i, 0] = 0
            self.theta_zegond_matrix[i, 1] = self.vector_3.theta_zegond
            self.theta_zegond_matrix[i, 2] = self.vector_4.theta_zegond
            self.theta_zegond_matrix[i, 3] = \
            self.transfer_case_5(self.vector_5.angular_velocity, self.vector_5.angular_acceleration)[1]
            self.theta_zegond_matrix[i, 4] = \
            self.transfer_case_6(self.vector_6.angular_velocity, self.vector_6.angular_acceleration)[1]

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

            # add steps to vector2.angle and also updates angular velocities and angular acceleration
            self.vector_2.update_theta(self.vector_2.angle + self.steps)
            QtWidgets.QApplication.processEvents()

        return self.angle_matrix, self.angular_velocity_matrix, self.angular_acceleration_matrix

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

    def transfer_case_5(self, omega, alpha):
        if self.vector_2.angular_velocity == 0:
            theta_prime_base_on_two = self.vector_5.theta_prime * self.vector_4.theta_prime
            theta_zegond_base_on_two = self.vector_5.theta_zegond * self.vector_4.theta_prime ** 2 + self.vector_5.theta_prime * self.vector_4.theta_zegond
        else:
            theta_prime_base_on_two = omega / self.vector_2.angular_velocity
            theta_zegond_base_on_two = (alpha - (
                        omega / self.vector_2.angular_velocity * self.vector_2.angular_acceleration)) / self.vector_2.angular_velocity ** 2
        return theta_prime_base_on_two, theta_zegond_base_on_two

    def transfer_case_6(self, omega, alpha):
        if self.vector_2.angular_velocity == 0:
            theta_prime_base_on_two = self.vector_6.theta_prime * self.vector_4.theta_prime
            theta_zegond_base_on_two = self.vector_6.theta_zegond * self.vector_4.theta_prime ** 2 + self.vector_6.theta_prime * self.vector_4.theta_zegond
        else:
            theta_prime_base_on_two = omega / self.vector_2.angular_velocity
            theta_zegond_base_on_two = (alpha - (
                        omega / self.vector_2.angular_velocity * self.vector_2.angular_acceleration)) / self.vector_2.angular_velocity ** 2
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
        if np.abs(la.norm(v_vector)) < 0.00000001 or np.abs(
                (la.norm(np.cross(v_vector, a_vector)) / la.norm(v_vector) ** 3)) < 0.0000000000001:
            radius_of_curvature = math.inf
        else:
            radius_of_curvature = (la.norm(np.cross(v_vector, a_vector)) / la.norm(v_vector) ** 3) ** (-1)
        if np.abs(norm_a_n_vector) < 0.00001:
            curvature_vector = array([0, math.inf])
        else:
            curvature_vector = (radius_of_curvature / norm_a_n_vector) * a_n_vector
        x_center_of_curvature = curvature_vector[0] + x
        y_center_of_curvature = curvature_vector[1] + y
        return x_center_of_curvature, y_center_of_curvature, radius_of_curvature

    def calculate_tangential_normal_vectors(self, v_x, v_y):
        r = np.sqrt(v_x ** 2 + v_y ** 2)
        tangential_vector = [v_x / r, v_y / r]
        normal_vector = [-v_y / r, v_x / r]
        return tangential_vector, normal_vector
