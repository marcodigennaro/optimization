from docplex.mp.model import Model
import numpy as np


class OptimalPowerFlow:
    """
    A class to model and solve the Optimal Power Flow (OPF) problem using CPLEX.

    This class handles the setup and solution of an OPF problem, which involves
    optimizing the power output of several generators to minimize the total cost
    of electricity production while meeting a given power demand and respecting
    generator limits and transmission constraints.

    Attributes:
        num_generators (int): Number of generators.
        cost_coeffs (list of tuples): Coefficients (a, b, c) for the cost function of each generator.
        min_output (list of float): Minimum power output for each generator.
        max_output (list of float): Maximum power output for each generator.
        demand (float): Total power demand that must be met.
        transmission_limits (dict): Max transmission capacity between each pair of generators.

    Methods:
        setup_problem(): Sets up the optimization model with the necessary variables, objective, and constraints.
        solve(): Solves the optimization model and prints the outputs and total cost.

    Example:
        >>> num_generators = 3
        >>> cost_coeffs = [(0.1, 14, 30), (0.15, 15, 25), (0.2, 10, 10)]
        >>> min_output = [10, 10, 10]
        >>> max_output = [100, 90, 80]
        >>> demand = 150
        >>> transmission_limits = {('1', '2'): 50, ('1', '3'): 50, ('2', '3'): 30}
        >>> opf = OptimalPowerFlow(num_generators, cost_coeffs, min_output, max_output, demand, transmission_limits)
        >>> opf.setup_problem()
        >>> opf.solve()
    """

    def __init__(self, num_generators, cost_coeffs, min_output, max_output, demand, transmission_limits):
        self.model = Model('OptimalPowerFlow')
        self.num_generators = num_generators
        self.cost_coeffs = cost_coeffs
        self.min_output = min_output
        self.max_output = max_output
        self.demand = demand
        self.transmission_limits = transmission_limits
        self.power = self.model.continuous_var_list(num_generators, lb=min_output, ub=max_output, name='Power')

    def setup_problem(self):
        """Set up the optimization problem with decision variables, objective function, and constraints."""
        # Objective: Minimize total cost
        total_cost = self.model.sum(self.cost_coeffs[i][0] * self.power[i] ** 2 +
                                    self.cost_coeffs[i][1] * self.power[i] +
                                    self.cost_coeffs[i][2] for i in range(self.num_generators))
        self.model.minimize(total_cost)

        # Constraint: Demand must be met
        self.model.add_constraint(self.model.sum(self.power) == self.demand, 'DemandSatisfaction')

        # Constraints: Transmission limits
        for i in range(self.num_generators):
            for j in range(i + 1, self.num_generators):
                self.model.add_constraint(self.model.abs(self.power[i] - self.power[j]) <=
                                          self.transmission_limits[f'{i + 1}', f'{j + 1}'],
                                          f'TransLimit_{i + 1}_{j + 1}')

    def solve(self):
        """Solve the model and display the outputs and the total cost if the solution is found."""
        solution = self.model.solve()
        if solution:
            print("Solution found:")
            for i in range(self.num_generators):
                print(f"Generator {i + 1} Output: {solution[self.power[i]]:.2f} MW")
            print(f"Total Generation Cost: ${solution.get_objective_value():.2f}")
        else:
            print("No solution found")



# Objective function (power loss)
def power_loss(d, rho, L, I):
    A = np.pi * (d**2) / 4  # cross-sectional area in square meters
    R = rho * L / A  # resistance in ohms
    P = I**2 * R  # power loss in watts
    return P


