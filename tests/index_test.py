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

@pytest.fixture
def single_target():
    return (-6.82186645, 39.301757704855774)

def test_get_bearing(index, origin, destination):
    assert index.get_bearing(origin, destination) == 156.90522903928954


def test_get_euclidean_distance(index, origin, destination):
    assert index.get_euclidean_distance(origin, destination) ==  0.06274428673887529


def test_get_great_circle_distance(index, origin, destination):
    assert index.get_great_circle_distance(origin, destination) ==  6969.148899790171


def test_get_distance(index, origin, destination):
    assert index.get_distance(origin, destination, 'euclidean') == 0.06274428673887529
    assert index.get_distance(origin, destination, 'great_circle') == 6969.148899790171


def test_geocode(index, single_target):
    assert index.geocode("Kigamboni Ferry Terminal") == single_target