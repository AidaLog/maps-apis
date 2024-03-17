import osmnx as ox
from typing import List, Tuple

class Index:
    def __init__(self):
        pass

    def get_bearing(self, origin: Tuple, destination: Tuple):
        """returns the bearing between two lat-long points as a single value in degrees

        Args:
            origin (tuple): origin lat-long point. example: (37.7749, -122.4194)
            destination (tuple): destination lat-long point example: (37.7749, -122.4194)

        Returns:
            bearing (float): the bearing(s) in decimal degrees
        """
        try:
            return ox.bearing.calculate_bearing(origin[0], origin[1], destination[0], destination[1])
        except:
            return -1
