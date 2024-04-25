import math
from optimization.core.wrappers import performance_measure
import pulp


def calc_total_cost(num_buses_30, num_buses_40):
    return (num_buses_30 * COST_30) + (num_buses_40 * COST_40)


@performance_measure
def bus_30_only():
    num_buses_30 = math.ceil(N_STUDENTS / SEAT_30)
    num_buses_40 = 0
    total_cost = calc_total_cost(num_buses_30, num_buses_40)

    return num_buses_30, num_buses_40, total_cost


@performance_measure
def bus_40_only():
    num_buses_30 = 0
    num_buses_40 = math.ceil(N_STUDENTS / SEAT_40)
    total_cost = calc_total_cost(num_buses_30, num_buses_40)

    return num_buses_30, num_buses_40, total_cost


@performance_measure
def educated_guess():
    # Number of 40-seats buses needed
    num_buses_40 = N_STUDENTS // SEAT_40

    remaining_students = N_STUDENTS - num_buses_40 * SEAT_40
    num_buses_30 = remaining_students // SEAT_30 + 1

    # Calculate total cost for this combination
    total_cost = calc_total_cost(num_buses_30, num_buses_40)

    return num_buses_30, num_buses_40, total_cost


@performance_measure
def iterative_solution(verbose=False):
    min_cost = float('inf')
    best_combination = None

    # Iterate over the number of 40-seat buses from 0 up to how many it would take if they were the only bus type used
    for num_buses_40 in range((N_STUDENTS // SEAT_40) + 1):

        # Calculate remaining students after using 40-seat buses
        seated_students = num_buses_40 * SEAT_40
        remaining_students = N_STUDENTS - seated_students

        if verbose:
            print(f'Testing {num_buses_40}*40-seats buses:')
            print(f'    {seated_students} students are seated')
            print(f'    {remaining_students} students are not seated')

        num_buses_30 = remaining_students // SEAT_30 + 1

        # Calculate total cost for this combination
        total_cost = calc_total_cost(num_buses_30, num_buses_40)

        # Check if this is the minimum cost found so far
        if total_cost < min_cost:
            min_cost = total_cost
            best_combination = (num_buses_30, num_buses_40, min_cost)
            if verbose:
                print(
                    f"        Best Combo: {best_combination[0]}x30-seaters, {best_combination[1]}x40-seaters at ${best_combination[2]} EUR")

        else:
            if verbose:
                print(f"        Price = {total_cost} EUR, discarding solution")
    return best_combination


@performance_measure
def linear_programming():
    # Define the problem
    prob = pulp.LpProblem("Bus_Allocation", pulp.LpMinimize)

    # Define the variables
    x = pulp.LpVariable('x', lowBound=0, cat=pulp.LpInteger)  # Number of 30-seat buses
    y = pulp.LpVariable('y', lowBound=0, cat=pulp.LpInteger)  # Number of 40-seat buses

    # Objective function
    prob += COST_30 * x + COST_40 * y, "Total Cost"

    # Constraints
    prob += SEAT_30 * x + SEAT_40 * y >= N_STUDENTS, "Seat Requirement"

    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    return int(x.value()), int(y.value()), pulp.value(prob.objective)
