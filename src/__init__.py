import osmnx as ox
from typing import List, Tuple

class Index:
    def __init__(self):
        pass

    def get_bearing(self, origin: Tuple, destination: Tuple) -> float:
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



    """Distance Calculation"""
    def get_euclidean_distance(self, origin: Tuple, destination: Tuple) -> float:
        """returns the distance between two lat-long points as a single value in meters

        Args:
            origin (tuple): origin lat-long point. example: (37.7749, -122.4194)
            destination (tuple): destination lat-long point example: (37.7749, -122.4194)

        Returns:
            distance (float): the distance in meters
        """
        try:
            return ox.distance.euclidean(origin[0], origin[1], destination[0], destination[1])
        except:
            return -1


    def get_great_circle_distance(self, origin: Tuple, destination: Tuple) -> float:
        """returns the distance between two lat-long points as a single value in meters

        Args:
            origin (tuple): origin lat-long point. example: (37.7749, -122.4194)
            destination (tuple): destination lat-long point example: (37.7749, -122.4194)

        Returns:
            distance (float): the distance in meters
        """
        try:
            return ox.distance.great_circle(origin[0], origin[1], destination[0], destination[1], earth_radius=6371009)
        except:
            return -1

    def get_distance(self, origin: Tuple, destination: Tuple, kind:str) -> float:
        """returns the distance between two lat-long points as a single value in meters

        Args:
            origin (tuple): origin lat-long point. example: (37.7749, -122.4194)
            destination (tuple): destination lat-long point example: (37.7749, -122.4194)
            kind (str): the kind of distance to calculate. options: 'euclidean', 'great_circle'

        Returns:
            distance (float): the distance in meters
        """
        try:
            if kind == 'euclidean':
                return self.get_euclidean_distance(origin, destination)
            elif kind == 'great_circle':
                return self.get_great_circle_distance(origin, destination)
        except:
            return -1




    """ Geocoding """
    def geocode(self, place_name:str) -> tuple:
        """returns the latitude and longitude of a place name

        Args:
            place_name (str): the name of the place. example: 'San Francisco, California'

        Returns:
            location (tuple): the latitude and longitude of the place. example: (37.7749, -122.4194)
        """
        try:
            return ox.geocoder.geocode(place_name)
        except:
            return ( )




    """ Graphs """
    def get_graph(self, place_name:str, network_type:str) -> object:
        """returns the street network for a place

        Args:
            place_name (str): the name of the place. example: 'Ubungo Maji, Dar Es Salaam, Tanzania'
            network_type (str): the type of street network to retrieve. options: 'drive', 'walk', 'bike', 'all'

        Returns:
            G (object): the street network object
        """
        try:
            return ox.graph_from_address(place_name, network_type=network_type)
        except:
            return None