from SolverClass import *
import matplotlib.pyplot as plt

vector_1 = KnownVector(length=0.2032, mass=0, inertia=0, angle=180) # mass and inertial is equal to zero
vector_2 = KnownVector(length=0.05715, mass=2, inertia=0.0067, angle=0, acceleration_ratio = 1)
vector_3 = UnKnownVector(length=0.18415, mass=5.5, inertia=0.0433)
vector_4 = UnKnownVector(length=0.1778, mass=2, inertia=0.2426)
vector_4_prime = UnKnownVector(length=0.127, mass=0, inertia = 0) ###### mass and inertial actually is not 0. just for debug
vector_1_prime = KnownVector(length=0.1016, mass = 0, inertia=0,  angle=180)
vector_5 = UnKnownVector(length=0.0508, mass=1.5, inertia=0.0009)
vector_6 = UnKnownVector(length=0.127, mass=6, inertia=0.0634)
spring = Spring(k=5000, free_length=0.15, max_deflection=0.002896)
damper = Damper(damping_coefficient=350)

initial_guess_loop_1 = np.array([63.95, 291.5])
initial_guess_loop_2 = np.array([140, 42.3])
step = 0.1
repeats = 3600


solver = SixLinkSolver(known_vectors=(vector_1, vector_1_prime, vector_2),
                       unknown_vectors=(vector_3, vector_4, vector_4_prime, vector_5, vector_6),
                       initial_guesses=(initial_guess_loop_1, initial_guess_loop_2), steps=step, num_of_repeats=repeats, spring=spring , damper=damper)
solver.calculate_angular_properties()

solver.writer_for_newton_method.save()
solver.writer_for_static.save()
solver.writer_for_energy.save()

# plt.plot(solver.angle_matrix[:,0], solver.energy_calculated_momentum[:, 0], label="momentum energy")
plt.plot(solver.angle_matrix[:,0], solver.energy_method_spring_term_matrix[:, 0], label="Spring term")
plt.plot(solver.angle_matrix[:,0], solver.energy_method_damper_term_matrix[:, 0], label="Damper term")
plt.plot(solver.angle_matrix[:,0], solver.sigma_a_energy_term_matrix[:, 0], label="equivalent inertia energy term")
# plt.plot(solver.angle_matrix[:,0], solver.equivalent_inertia_matrix[:, 0], label="equivalent inertia")
# plt.plot(solver.angle_matrix[:,0], solver.sigma_b_matrix[:, 0], label="sigma B")
plt.plot(solver.angle_matrix[:,0], solver.sigma_potential_term_matrix[:, 0], label="Potential term")
plt.plot(solver.angle_matrix[:,0], solver.sigma_b_energy_term_matrix[:, 0], label="Sigma b energy term")


# plt.plot(solver.angle_matrix[:,0], solver.dynamic_method_forces_matrix[:, 14], label="momentum dynamic")
# plt.plot(solver.angle_matrix[:,0], solver.energy_calculated_momentum[:, 0], label="momentum energy")
# plt.plot(solver.angle_matrix[:,0], solver.static_method_forces_matrix[:, 14], label="momentum static")
# print(solver.vector_2.minimum_r, solver.vector_3.minimum_r, solver.vector_4.minimum_r, solver.vector_5.minimum_r, solver.vector_6.minimum_r)
print(np.max(np.abs(solver.vector_2.angular_velocity)))
print(solver.vector_2.minimum_r, solver.vector_3.minimum_r, solver.vector_4.minimum_r, solver.vector_5.minimum_r, solver.vector_6.minimum_r)
plt.xlabel('Theta 2')
plt.ylabel('Energy Terms in Momentum equation (N.m)')
plt.legend(loc=1)
plt.show()

