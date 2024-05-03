import warnings

from scipy.optimize import minimize
import numpy as np
from pydantic import BaseModel


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
        self.n_consumers = None
        self.n_sources = None
        self.sources = {}  # Dictionary to store energy sources
        self.consumers = {}  # Dictionary to store consumers
        self.flows = {}  # Dictionary to track energy flow from sources to consumers
        

    def add_source(self, source):
        """
        Add an energy source to the distribution system.

        Args:
            source (EnergySource): EnergySource object to be added.

        Raises:
            KeyError: If the key (source name) already exists in the sources dictionary.
        """
        if source.name in self.sources.keys():
            raise KeyError(f'The key {source.name} exists already')

        self.sources[source.name] = {'capacity': source.capacity,
                                     'cost_per_unit': source.cost_per_unit,
                                     'unit': source.unit}
        self.n_sources = len(self.sources)
        
    def add_consumer(self, consumer):
        """
        Add a consumer to the distribution system.

        Args:
            consumer (Consumer): Consumer object to be added.

        Raises:
            KeyError: If the key (consumer name) already exists in the consumers dictionary.
        """
        if consumer.name in self.consumers.keys():
            raise KeyError(f'The key {consumer.name} exists already')

        self.consumers[consumer.name] = {'demand': consumer.demand}
        self.n_consumers = len(self.consumers)

    def cost_function(self, x):
        total_cost = 0
        for source_name, source_data in self.sources.items():
            for consumer_name, consumer_data in self.consumers.items():
                cost_per_unit = source_data['cost_per_unit']
                demand = consumer_data['demand']
                total_cost += cost_per_unit * x[source_name][consumer_name]
        return total_cost

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

    def optimize_flow(self):
        # Initialize flows
        x0 = {source_name: {consumer_name: 0 for consumer_name in self.consumers} for source_name in self.sources}

        # Define constraints
        cons = [
            {'type': 'eq', 'fun': lambda x: self.demand_constraint(x)},
            {'type': 'ineq', 'fun': lambda x: self.capacity_constraint(x)}
        ]

        # Minimize objective function
        res = minimize(self.objective_function, x0, constraints=cons, options={'disp': True})
        if not res.success:
            raise ValueError("Optimization failed")

        return res.fun, res.x

    def calculate_cost(self, x_array):

        assert x_array[0::2].sum() <= self.sources['Solar']['capacity']
        if x_array[1::2].sum() > self.sources['Wind']['capacity']:
            warnings.warn(f'{x_array[1::2].sum()} obtained on second column, and is too big')
        return self.sources['Solar']['cost_per_unit'] * x_array[0::2].sum() + \
            self.sources['Wind']['cost_per_unit'] * x_array[1::2].sum()
