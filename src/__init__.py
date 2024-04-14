import osmnx as ox
from warnings import filterwarnings
import logging


filterwarnings("ignore")


class Index:
    def __init__(self):
        pass

    def get_bearing(self, origin: tuple, destination: tuple) -> float:
        """returns the bearing between two lat-long points as a single value in degrees

        Args:
            origin (tuple): origin lat-long point. example: (37.7749, -122.4194)
            destination (tuple): destination lat-long point example: (37.7749, -122.4194)

        Returns:
            bearing (float): the bearing(s) in decimal degrees
        """
        try:
            return ox.bearing.calculate_bearing(origin[0], origin[1], destination[0], destination[1])
        except Exception as e:
            logging.error(f"Error occurred while calculating bearing: {e}")
            return -1



    """Distance Calculation"""
    def get_euclidean_distance(self, origin: tuple, destination: tuple) -> float:
        """returns the distance between two lat-long points as a single value in meters

        Args:
            origin (tuple): origin lat-long point. example: (37.7749, -122.4194)
            destination (tuple): destination lat-long point example: (37.7749, -122.4194)

        Returns:
            distance (float): the distance in meters
        """
        try:
            return ox.distance.euclidean(origin[0], origin[1], destination[0], destination[1])
        except Exception as e:
            logging.error(f"Error occurred while calculating euclidean distance: {e}")
            return -1


    def get_great_circle_distance(self, origin: tuple, destination: tuple) -> float:
        """returns the distance between two lat-long points as a single value in meters

        Args:
            origin (tuple): origin lat-long point. example: (37.7749, -122.4194)
            destination (tuple): destination lat-long point example: (37.7749, -122.4194)

        Returns:
            distance (float): the distance in meters
        """
        try:
            return ox.distance.great_circle(origin[0], origin[1], destination[0], destination[1], earth_radius=6371009)
        except Exception as e:
            logging.error(f"Error occurred while calculating GCD: {e}")
            return -1

    def get_distance(self, origin: tuple, destination: tuple, kind:str) -> float:
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
        except Exception as e:
            logging.error(f"Error occurred while getting distance: {e}")
            return -1


    def get_center(self, origin:tuple, destination:tuple) -> tuple:
        """returns the center of two lat-long points

        Args:
            origin (tuple): origin lat-long point. example: (37.7749, -122.4194)
            destination (tuple): destination lat-long point example: (37.7749, -122.4194)

        Returns:
            center (tuple): the center lat-long point
        """
        latitude_center = (origin[0] + destination[0]) / 2
        longitude_center = (origin[1] + destination[1]) / 2
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
        except Exception as e:
            logging.error(f"Failed to geocode {place_name} : {e}")
            return ()




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
        except Exception as e:
            logging.error(f"Error while retrieving Graph for {place_name}: {e}")
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

    def get_shortest_route(self, origin: tuple, destination:tuple, mode:str, weight:str) -> any:
        """returns the shortest route between two lat-long points

        Args:
            origin (tuple): origin lat-long point. example: (37.7749, -122.4194)
            destination (tuple): destination lat-long point example: (37.7749, -122.4194)
            mode (str): the type of street network to retrieve. options: 'drive', 'walk', 'bike', 'all'
            weight (str): 'time', 'length', 'cost', 'speed', 'elevation'

        Returns:
            route (list): the shortest route as a list of lat-long points
        """
        try:
            G = ox.graph_from_point(
                self.get_center(
                    origin=origin,
                    destination=destination),
                dist=self.get_distance(
                    origin=origin,
                    destination=destination,
                    kind='great_circle'),
                network_type=mode)

            node_point1=ox.nearest_nodes(G,origin[1],origin[0])
            node_point2=ox.nearest_nodes(G,destination[1],destination[0])
            return G, ox.shortest_path(G, node_point1, node_point2, weight=weight)
        except Exception as e:
            logging.error(f"Error occurred while getting shortest distance from {origin}, to {destination}: {e}")
            return None, None

    def get_road_distance(
        self,
        origin: tuple,
        destination:tuple,
        mode:str,
        weight:str) -> float:

        """returns the distance between two lat-long points by following roads

        Args:
            origin (tuple): origin lat-long point. example: (37.7749, -122.4194)
            destination (tuple): destination lat-long point example: (37.7749, -122.4194)
            mode (str): the type of street network to retrieve. options: 'drive', 'walk', 'bike', 'all'
            weight (str): 'time', 'length', 'cost', 'speed', 'elevation'

        Returns:
            distance (float): the distance in meters
        """
        G, shortest_path = self.get_shortest_route(origin, destination, mode, weight)
        if shortest_path is None:
            return -1

        total_distance = 0
        for i in range(len(shortest_path)-1):
            u, v = shortest_path[i], shortest_path[i+1]
            total_distance += G[u][v][0]['length']

        return total_distance