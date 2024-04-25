# test_bus_allocation.py
import pytest
from optimization.core.bus_allocation import BusAllocation


@pytest.fixture
def bus_allocation():
    """Fixture to create a BusAllocation instance with predefined configuration."""
    return BusAllocation(seat_config=(30, 40, 50), cost_config=(300, 400, 500), n_students=100)


def test_trivial_solution(bus_allocation):
    result = bus_allocation.trivial_solution()
    assert isinstance(result, dict), "Result should be a dictionary."
    assert set(result.keys()) == {'A', 'B', 'C'}, "Keys should exactly be 'A', 'B', and 'C'."


def test_educated_guess(bus_allocation):
    result = bus_allocation.educated_guess()
    assert isinstance(result, dict), "Result should be a dictionary."
    assert set(result.keys()) == {'A', 'B', 'C'}, "Keys should exactly be 'A', 'B', and 'C'."


def test_linear_programming(bus_allocation):
    result = bus_allocation.linear_programming()
    assert isinstance(result, dict), "Result should be a dictionary."
    assert set(result.keys()) == {'A', 'B', 'C'}, "Keys should exactly be 'A', 'B', and 'C'."


def test_iterative_solution(bus_allocation):
    result = bus_allocation.iterative_solution()
    assert isinstance(result, dict), "Result should be a dictionary."
    assert set(result.keys()) == {'A', 'B', 'C'}, "Keys should exactly be 'A', 'B', and 'C'."
