import math
from optimization.core.wrappers import performance_measure, print_output
import pulp


class BusAllocation:
    """
    A class to handle bus allocation problems for transporting students.
    """

    def __init__(self, seat_config, cost_config, n_students):
        """
        Initializes the BusAllocation class with seat and cost configurations for buses.

        Parameters:
            seat_config (tuple): Tuple containing the seat capacity for bus_A, bus_B, and bus_C.
            cost_config (tuple): Tuple containing the cost for bus_A, bus_B, and bus_C.
            n_students (int): Total number of students to transport.
        """
        self.seat_a, self.seat_b, self.seat_c = seat_config
        self.cost_a, self.cost_b, self.cost_c = cost_config
        self.n_students = n_students

    def calc_total_cost(self, num_bus_a, num_bus_b, num_bus_c):

        """
        Calculates the total cost based on the number of each type of bus used.

        Parameters:
            num_bus_a (int): Number of bus_A used.
            num_bus_b (int): Number of bus_B used.
            num_bus_c (int): Number of bus_C used.

        Returns:
            int: Total cost of using the buses.
        """
        return (num_bus_a * self.cost_a) + (num_bus_b * self.cost_b) + (num_bus_c * self.cost_c)

    @print_output
    @performance_measure
    def trivial_solution(self, bus='A'):
        print(bus)
        num_bus_a: int = 0
        num_bus_b: int = 0
        num_bus_c: int = 0
        if bus == 'A':
            num_bus_a = math.ceil( self.n_students / self.seat_a )
        elif bus == 'B':
            num_bus_b = math.ceil( self.n_students / self.seat_b )
        elif bus == 'C':
            num_bus_c = math.ceil( self.n_students / self.seat_c )
        total_cost = self.calc_total_cost(num_bus_a, num_bus_b, num_bus_c)

        result_dict = {
            'num_buses_A': num_bus_a,
            'num_buses_B': num_bus_b,
            'num_buses_C': num_bus_c,
            'minimum_total_cost': total_cost
        }

        return result_dict

    @performance_measure
    @print_output
    def educated_guess(self):
        """
        Provides an educated guess solution where bus_A is only used after filling bus_B and bus_C.

        Returns:
            tuple: Tuple containing number of each type of bus used and the total cost.
        """
        num_bus_c = self.n_students // self.seat_c
        remaining_students = self.n_students - num_bus_c * self.seat_c
        num_bus_b = remaining_students // self.seat_b
        remaining_students -= num_bus_b * self.seat_b
        num_bus_a = math.ceil(remaining_students / self.seat_a)

        total_cost = self.calc_total_cost(num_bus_a, num_bus_b, num_bus_c)

        result_dict = {
            'num_buses_A': num_bus_a,
            'num_buses_B': num_bus_b,
            'num_buses_C': num_bus_c,
            'minimum_total_cost': total_cost
        }

        return result_dict

    @performance_measure
    @print_output
    def linear_programming(self):
        """
        Solves the bus allocation problem using linear programming to minimize cost.

        Returns:
            tuple: Tuple containing the number of each type of bus used and the total cost.
        """
        prob = pulp.LpProblem("Bus_Allocation", pulp.LpMinimize)
        x = pulp.LpVariable('x', lowBound=0, cat=pulp.LpInteger)  # Number of bus_A
        y = pulp.LpVariable('y', lowBound=0, cat=pulp.LpInteger)  # Number of bus_B
        z = pulp.LpVariable('z', lowBound=0, cat=pulp.LpInteger)  # Number of bus_C

        prob += self.cost_a * x + self.cost_b * y + self.cost_c * z, "Total Cost"
        prob += self.seat_a * x + self.seat_b * y + self.seat_c * z >= self.n_students, "Seat Requirement"

        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        result_dict = {
            'num_buses_A': int(x.value()),
            'num_buses_B': int(y.value()),
            'num_buses_C': int(z.value()),
            'minimum_total_cost': pulp.value(prob.objective)
        }

        return result_dict

    @performance_measure
    @print_output
    def iterative_solution(self, verbose=False):
        """
        Iteratively explores all combinations of bus uses to find the one with the minimum cost.

        Parameters:
            verbose (bool): If True, prints detailed debug information.

        Returns:
            tuple: Tuple containing the number of each type of bus used and the minimum cost found.
        """
        min_cost = float('inf')
        best_combination = None

        # Calculate the max number of each bus type if used exclusively
        max_bus_c = self.n_students // self.seat_c
        max_bus_b = self.n_students // self.seat_b
        max_bus_a = self.n_students // self.seat_a

        # Iterate over all combinations of bus_C, bus_B, and bus_A
        for num_bus_c in range(max_bus_c + 1):
            for num_bus_b in range(max_bus_b + 1):
                for num_bus_a in range(max_bus_a + 1):
                    seated_students = (num_bus_c * self.seat_c) + (num_bus_b * self.seat_b) + (num_bus_a * self.seat_a)

                    if seated_students >= self.n_students:
                        total_cost = self.calc_total_cost(num_bus_a, num_bus_b, num_bus_c)
                        if total_cost < min_cost:
                            min_cost = total_cost
                            best_combination = (num_bus_a, num_bus_b, num_bus_c, min_cost)

                            if verbose:
                                print(
                                    f"Testing {num_bus_c}*{self.seat_c}-seats, {num_bus_b}*{self.seat_b}-seats, {num_bus_a}*{self.seat_a}-seats:")
                                print(f"    {seated_students} students are seated, Total cost = {total_cost} EUR")
                                print(
                                    f"        Best Combo: {num_bus_a}x{self.seat_a}-seaters, {num_bus_b}x{self.seat_b}-seaters, {num_bus_c}*{self.seat_c}-seaters at ${total_cost} EUR")
                        elif verbose:
                            print(f"    Price = {total_cost} EUR, discarding solution")

        result_dict = {
            'num_buses_A': best_combination[0],
            'num_buses_B': best_combination[1],
            'num_buses_C': best_combination[2],
            'minimum_total_cost': best_combination[3]
        }

        return result_dict
