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


def test_get_bearing(index, origin, destination):
    assert index.get_bearing(origin, destination) == 156.90522903928954


