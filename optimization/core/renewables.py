import warnings
import numpy as np
from pydantic import BaseModel
import math


class ConsumerModel(BaseModel):
    """Data model representing a consumer."""
    name: str  # Name of the consumer
    demand: float  # Demand of the consumer (in units)


class SourceModel(BaseModel):
    """Data model representing an energy source."""
    name: str  # Name of the energy source
    capacity: int  # Capacity of the energy source (in units)
    cost_per_unit: float  # Cost per unit of energy from the source
    unit: str  # Unit of the energy source (default: 'kW')


class EnergySource:
    """Represents an energy source."""

    def __init__(self, name, capacity, cost_per_unit, unit='kW'):
        """
        Initialize an EnergySource object.

        Args:
            name (str): Name of the energy source.
            capacity (int): Capacity of the energy source (in units).
            cost_per_unit (float): Cost per unit of energy from the source.
            unit (str, optional): Unit of the energy source (default: 'kW').
        """
        self.name = name
        self.capacity = capacity
        self.cost_per_unit = cost_per_unit
        self.unit = unit


class Consumer:
    """Represents a consumer."""

    def __init__(self, name, demand):
        """
        Initialize a Consumer object.

        Args:
            name (str): Name of the consumer.
            demand (float): Demand of the consumer (in units).
        """
        self.name = name
        self.demand = demand


class EnergyDistribution:
    """Manages energy sources, consumers, and flows."""

    def __init__(self):
        """Initialize an EnergyDistribution object."""
        self.D_B = None
        self.D_A = None
        self.W_max = None
        self.S_max = None
        self.n_consumers = None
        self.n_sources = None
        self.sources = {}  # Dictionary to store energy sources
        self.consumers = {}  # Dictionary to store consumers

    def read_max_values(self):
        self.S_max = self.sources['Solar']['capacity']
        self.W_max = self.sources['Wind']['capacity']
        self.D_A = self.consumers['A']['demand']
        self.D_B = self.consumers['B']['demand']

    def add_source(self, source):
        """
        Add an energy source to the distribution system.

        Args:
            source (EnergySource): EnergySource object to be added.

        Raises:
            KeyError: If the key (source name) already exists in the sources' dictionary.
        """
        if source.name in self.sources.keys():
            raise KeyError(f'The key {source.name} exists already')

        self.sources[source.name] = {'capacity': source.capacity,
                                     'cost_per_unit': source.cost_per_unit,
                                     'unit': source.unit}

        self.n_sources = len(self.sources)

        return

    def add_consumer(self, consumer):
        """
        Add a consumer to the distribution system.

        Args:
            consumer (Consumer): Consumer object to be added.

        Raises:
            KeyError: If the key (consumer name) already exists in the consumers' dictionary.
        """
        if consumer.name in self.consumers.keys():
            raise KeyError(f'The key {consumer.name} exists already')

        self.consumers[consumer.name] = {'demand': consumer.demand}
        self.n_consumers = len(self.consumers)

        return

    def demand_constraint(self, x):
        constraints = []
        for consumer_name, consumer_data in self.consumers.items():
            demand = consumer_data['demand']
            total_flow = sum(x[source_name][consumer_name] for source_name in self.sources)
            constraints.append(demand - total_flow)
        return constraints

    def capacity_constraint(self, x):
        constraints = []
        for source_name, source_data in self.sources.items():
            capacity = source_data['capacity']
            total_flow = sum(x[source_name][consumer_name] for consumer_name in self.consumers)
            constraints.append(capacity - total_flow)
        return constraints

    def check_solution_integrity(self, solution, tolerance=1e-9):
        """Test that the proposed solution satisfies the problem requirements"""

        solar_demand, wind_demand, A_demand, B_demand = calculate_local_demand(solution)

        #if solar_demand > self.S_max:
        #    warnings.warn(
        #        f'Total solar demand ({solar_demand}) is higher than capacity ({S_max}).')
        #if wind_demand > self.W_max:
        #    warnings.warn(
        #        f'Total wind demand ({wind_demand}) is higher than capacity ({W_max}).')

        if not math.isclose(A_demand, self.D_A):
            raise ValueError(f"Customer A's demand is not met ({A_demand}!={self.consumers['A']['demand']})")
        if not math.isclose(B_demand, self.D_B):
            raise ValueError(f"customer B's demand is not met ({B_demand}!={self.consumers['B']['demand']})")
        if solar_demand - self.S_max > tolerance:
            raise ValueError(f"Total Solar demand exceeds Solar capacity ({solar_demand}>{self.S_max}")
        if wind_demand - self.W_max > tolerance:
            raise ValueError(f"Total Wind demand exceeds Wind capacity ({wind_demand}>{self.W_max}")

        return True

    def cost_function(self, solution, test=False):

        # Test input correctness
        if test:
            self.check_solution_integrity(solution)

        solar_demand, wind_demand, A_demand, B_demand = calculate_local_demand(solution)

        return self.sources['Solar']['cost_per_unit'] * solar_demand + \
            self.sources['Wind']['cost_per_unit'] * wind_demand

    def generate_one_solution(self):

        a = np.random.uniform(0, self.D_A)
        b = self.D_A - a

        # Possible range for c based on a + c < S_max
        max_c = self.S_max - a

        # Random float for c such that a + c < S_max and c < max_c
        c = np.random.uniform(0, min(max_c, self.S_max))
        d = self.D_B - c

        solution = np.array([[a, b], [c, d]])

        # if any value is negative repeat
        if (solution < 0).any():
            return self.generate_one_solution()

        # Check integrity of solution, else repeat
        try:
            self.check_solution_integrity(solution)
        except ValueError:
            return self.generate_one_solution()

        # Check column 1 constraint (b + d < W_max)
        if b + d > self.W_max:
            return self.generate_one_solution()

        return solution

    def generate_many_solutions(self, nsolutions=1000):

        solutions = []
        costs = []
        solution_hashes = set()  # To store hashes of arrays for quick membership checks

        for _ in range(nsolutions):
            solution = self.generate_one_solution()
            solution_tuple = tuple(map(tuple, solution))  # Convert array to a tuple of tuples

            if solution_tuple not in solution_hashes:
                cost = self.cost_function(solution)
                costs.append(cost)
                solutions.append(solution)
                solution_hashes.add(solution_tuple)  # Store the hashable version
            else:
                print('Solution already present')

        return solutions, costs


def calculate_local_demand(solution):
    # Input is a vector
    if solution.ndim == 1:
        solar_demand = solution[0::2].sum()
        wind_demand = solution[1::2].sum()
        A_demand = solution[:2].sum()
        B_demand = solution[2:].sum()

        # Input is a matrix
    elif solution.ndim == 2:
        solar_demand = solution[:, 0].sum()
        wind_demand = solution[:, 1].sum()
        A_demand = solution[0, :].sum()
        B_demand = solution[1, :].sum()

    else:
        raise ValueError(f"Incorrect input shape = {solution.shape}")

    return solar_demand, wind_demand, A_demand, B_demand
