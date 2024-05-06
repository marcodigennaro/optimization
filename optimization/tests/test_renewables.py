import pytest
import numpy as np
from optimization.core.renewables import EnergyDistribution, EnergySource, Consumer


@pytest.fixture
def energy_distribution():
    """Fixture to create an empty EnergyDistribution object."""

    # Create Source instances
    solar = EnergySource("Solar", 100, 0.10)
    wind = EnergySource("Wind", 150, 0.05)

    # Create Consumer instances
    consumer_a = Consumer("A", 3.)
    consumer_b = Consumer("B", 5.)

    # Create the energy distribution system
    system = EnergyDistribution()

    system.add_source(solar)
    system.add_source(wind)

    system.add_consumer(consumer_a)
    system.add_consumer(consumer_b)

    return system


@pytest.fixture
def guess_solution():
    return np.array([[1.5, 1.5], [2., 3.]])


def test_add_source(energy_distribution):
    """ Assert that the source has been added correctly """
    assert "Solar" in energy_distribution.sources.keys()
    assert "Wind" in energy_distribution.sources.keys()

    assert energy_distribution.sources["Solar"] == {'capacity': 100, 'cost_per_unit': 0.10, 'unit': 'kW'}
    assert energy_distribution.sources["Wind"] == {'capacity': 150, 'cost_per_unit': 0.05, 'unit': 'kW'}


def test_add_consumer(energy_distribution):
    """ Assert that consumers has been added correctly """

    assert {'A', 'B'} == set(energy_distribution.consumers.keys())
    assert energy_distribution.consumers["A"] == {'demand': 3.}
    assert energy_distribution.consumers["B"] == {'demand': 5.}


def test_cost_function(energy_distribution, guess_solution):
    """ Assert correctness of cost function calculation given a guess solution"""

    assert energy_distribution.cost_function(guess_solution) == pytest.approx(0.575)


def test_power_requirements(energy_distribution):
    """ Test that the sum of all demands remains lower than the minimum of generated power"""

    assert sum([energy_distribution.consumers[k]['demand'] for k in energy_distribution.consumers]) <= min(
        [energy_distribution.sources[k]['capacity'] for k in energy_distribution.sources])


def test_input_cost_shape(energy_distribution, guess_solution):
    """ Test that calculate_cost() works for vectors and for matrices"""

    assert energy_distribution.cost_function(guess_solution) == \
           energy_distribution.cost_function(guess_solution.flatten())
