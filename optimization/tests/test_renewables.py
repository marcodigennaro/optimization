import pytest
from optimization.core.renewables import EnergyDistribution, EnergySource, Consumer


@pytest.fixture
def energy_distribution():
    """Fixture to create an empty EnergyDistribution object."""
    return EnergyDistribution()


def test_add_source(energy_distribution):
    """Test adding a source to the energy distribution system."""
    # Create a source
    source = EnergySource(name="Solar", capacity=100, cost_per_unit=0.10)

    # Add the source to the energy distribution system
    energy_distribution.add_source(source)

    # Assert that the source has been added correctly
    assert "Solar" in energy_distribution.sources.keys()
    assert energy_distribution.sources["Solar"] == {'capacity': 100, 'cost_per_unit': 0.10, 'unit': 'kW'}


def test_add_consumer(energy_distribution):
    """Test adding a consumer to the energy distribution system."""
    # Create a consumer
    consumer = Consumer(name="Consumer A", demand=90)

    # Add the consumer to the energy distribution system
    energy_distribution.add_consumer(consumer)

    # Assert that the consumer has been added correctly
    assert "Consumer A" in energy_distribution.consumers.keys()
    assert energy_distribution.consumers["Consumer A"] == {'demand': 90}
