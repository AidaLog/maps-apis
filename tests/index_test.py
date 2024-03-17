import pytest
from src import Index



@pytest.fixture
def index():
    return Index()

@pytest.fixture
def origin():
    return (-6.8096036,39.2854829)

@pytest.fixture
def destination():
    return (-6.867255,39.310245)


def test_get_bearing(index):
    origin = (37.7749, -122.4194)
    destination = (37.78369666906259, -122.41703415761295)

    assert index.get_bearing(origin, destination) == 11.999999999975099