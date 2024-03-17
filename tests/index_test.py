import pytest
from src import Index



@pytest.fixture
def index():
    return Index()


def test_get_bearing(index):
    origin = (37.7749, -122.4194)
    destination = (37.78369666906259, -122.41703415761295)

    assert index.get_bearing(origin, destination) == 12