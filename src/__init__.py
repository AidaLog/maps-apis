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


    def get_center(self, source:tuple, destination:tuple):
        """returns the center of two lat-long points

        Args:
            source (tuple): source lat-long point. example: (37.7749, -122.4194)
            destination (tuple): destination lat-long point example: (37.7749, -122.4194)

        Returns:
            center (tuple): the center lat-long point
        """
        latitude_center = (source[0] + destination[0]) / 2
        longitude_center = (source[1] + destination[1]) / 2
        return (latitude_center, longitude_center)


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
    def get_graph(self, place_name:str, network_type:str, kind:str = "address") -> object:
        """returns the street network for a place

        Args:
            place_name (str): the name of the place. example: 'Ubungo Maji, Dar Es Salaam, Tanzania'
            network_type (str): the type of street network to retrieve. options: 'drive', 'walk', 'bike', 'all'

        Returns:
            G (object): the street network object
        """
        try:
            if kind == "address":
                return ox.graph_from_address(place_name, network_type=network_type)
            elif kind == "place":
                return ox.graph_from_place(place_name, network_type=network_type)
        except:
            return None

    def get_graph_from_points(self, points: list[tuple], network_type:str, mode:str) -> object:
        """returns the street network for a place

        Args:
            points (tuple): the latitude and longitude of the place. example: [(37.7749, -122.4194), (37.7749, -122.4194)]
            mode (str): the type of street network to retrieve. options: 'drive', 'walk', 'bike', 'all'
            network_type (str): bbox, points

        Returns:
            G (object): the street network object
        """
        pass


    def get_road_distance(self, p1_address:str, p2_address:str, mode:str) -> float:
        """returns the distance between two addresses by following roads

        Args:
            p1_address (str): the first address. example: 'Ubungo Maji, Dar Es Salaam, Tanzania'
            p2_address (str): the second address. example: 'Mbezi, Dar Es Salaam, Tanzania'
            mode (str): the mode of transportation. options: 'drive', 'walk', 'bike'

        Returns:
            distance (float): the distance in meters
        """
        # try:
        G1 = self.get_graph(p1_address, mode)
        G2 = self.get_graph(p2_address, mode)

        print("G1: ", G1, "Type: ", type(G1))
        print("G2: ", G2, "Type: ", type(G2))

        point1 = (G1.nodes[list(G1.nodes())[0]]['y'], G1.nodes[list(G1.nodes())[0]]['x'])
        point2 = (G2.nodes[list(G2.nodes())[0]]['y'], G2.nodes[list(G2.nodes())[0]]['x'])
        print("Point1: ", point1)
        print("Point2: ", point2)

        return self.get_distance(point1, point2, 'great_circle')
        # except:
        #     return -1