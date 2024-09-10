import os
import httpx
import asyncio
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import logging
from warnings import filterwarnings

import concurrent.futures
from functools import lru_cache

import json
from datetime import datetime



filterwarnings("ignore")


class Index:
    def __init__(self):
        pass

    @lru_cache(maxsize=None)
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


    @lru_cache(maxsize=None)
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



    @lru_cache(maxsize=None)
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


    @lru_cache(maxsize=None)
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


    @lru_cache(maxsize=None)
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


    @lru_cache(maxsize=None)
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


    @lru_cache(maxsize=None)
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


    @lru_cache(maxsize=None)
    def get_graph_from_points(self, points: list[tuple], network_type:str, mode:str) -> object:
        """returns the street network for a place

        Args:
            points (tuple): the latitude and longitude of the place. example: [(37.7749, -122.4194), (37.7749, -122.4194)]
            mode (str): the type of street network to retrieve. options: 'drive', 'walk', 'bike', 'all'
            network_type (str): bbox, points

        Returns:
            G (object): the street network object
        """
        try:
            if network_type == "points":
                # Get the center of the points
                center_point = (
                    sum(point[0] for point in points) / len(points),
                    sum(point[1] for point in points) / len(points)
                )
                # Calculate the radius from the center to the farthest point
                radius = max(ox.utils.euclidean_dist_vec(center_point[0], center_point[1], point[0], point[1]) for point in points)
                # Retrieve the graph from point with the specified radius and network type
                return ox.graph_from_point(center_point, dist=radius, network_type=mode)
            elif network_type == "bbox":
                # Calculate the bounding box from the points
                north, south = max(point[0] for point in points), min(point[0] for point in points)
                east, west = max(point[1] for point in points), min(point[1] for point in points)
                # Retrieve the graph from the bounding box and network type
                return ox.graph_from_bbox(north, south, east, west, network_type=mode)
        except Exception as e:
            logging.error(f"Error occurred while getting graph from points: {e}")
            return None


    @lru_cache(maxsize=None)
    def get_graph_from_bbox(self, north:float, south:float, east:float, west:float, network_type:str="drive") -> object:
        """returns the street network for a place

        Args:
            north (float): the northernmost latitude
            south (float): the southernmost latitude
            east (float): the easternmost longitude
            west (float): the westernmost longitude
            network_type (str): the type of street network to retrieve. options: 'drive', 'walk', 'bike', 'all'

        Returns:
            G (object): the street network object
        """
        try:
            return ox.graph_from_bbox(north, south, east, west, network_type=network_type)
        except Exception as e:
            logging.error(f"Error occurred while getting graph from bbox: {e}")
            return None

    @lru_cache(maxsize=None)
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
    
    
    @staticmethod
    def save_graph(graph, graph_name: str, network_type: str) -> dict:
        """
        Static method to save graph to local memory in directory <network_type>/graph_name
        and create a metadata file.

        Parameters:
        - graph: The graph to be saved.
        - graph_name: The name of the graph file (without extension).
        - network_type: The type of network (e.g., 'walk', 'drive').
        """
        if graph is None:
            raise ValueError("The graph object is None. Please ensure it was created successfully.")
        
        # Create directory path
        directory = os.path.join("Graph_Network", graph_name, network_type)
        
        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Define file paths
        graph_file_path = os.path.join(directory, f"{graph_name}.graphml")
        metadata_file_path = os.path.join(directory, f"{graph_name}_metadata.json")
        
        # Save the graph
        ox.save_graphml(graph, filepath=graph_file_path)
        
        # Create metadata
        metadata = {
            "graph_name": graph_name,
            "network_type": network_type,
            "file_path": graph_file_path,
            "date_created": datetime.now().isoformat()
        }
        
        # Save metadata to JSON
        with open(metadata_file_path, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=4)
        
        return metadata
    

    @staticmethod
    def load_graph(graph_name: str, network_type: str):
        """
        Static method to load a graph from local memory from directory <network_type>/graph_name
        
        Parameters:
        - graph_name: The name of the graph file (without extension).
        - network_type: The type of network (e.g., 'walk', 'drive').

        Returns:
        - graph: The loaded graph object.
        """
        directory = os.path.join("Graph_Network", graph_name, network_type)
        graph_file_path = os.path.join(directory, f"{graph_name}.graphml")
        
        if not os.path.exists(graph_file_path):
            raise FileNotFoundError(f"The graph file '{graph_file_path}' does not exist.")
        graph = ox.load_graphml(filepath=graph_file_path)
        
        return graph
    
    
    @staticmethod
    def visualize_network(graph,  file_name: str="graph_visualization", output_dir: str="samples"):
        """
        Visualize the network graph using networkx and matplotlib.

        Parameters:
        - graph: The network graph to be visualized (a networkx.Graph or similar object).
        """
        if graph is None:
            raise ValueError("The graph object is None. Please ensure it was loaded successfully.")
        
        if isinstance(graph, nx.MultiGraph) or isinstance(graph, nx.Graph):
            G = graph
        else:
            G = ox.utils_graph.get_undirected(graph)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        file_path = os.path.join(output_dir, file_name)
        
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(G, k=0.15, iterations=20)
        nx.draw(G, pos, with_labels=True, node_size=10, node_color='blue', edge_color='gray', alpha=0.7)
        plt.title('Network Visualization')
        
        plt.savefig(file_path)
        plt.close()
        
        print(f"Graph visualization saved to {file_path}")
        return file_path


    @staticmethod
    def get_route(start_coords, end_coords):
        """
        Get route information from OSRM using HTTPX.

        Parameters:
        - start_coords: Tuple of (latitude, longitude) for the start point.
        - end_coords: Tuple of (latitude, longitude) for the end point.

        Returns:
        - distance: The distance of the route in meters.
        - duration: The estimated travel time in seconds.
        """
        osrm_url = (
            "http://router.project-osrm.org/route/v1/driving/"
            f"{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}"
            "?overview=false"
        )

        async def fetch_route():
            async with httpx.AsyncClient() as client:
                response = await client.get(osrm_url)
                response.raise_for_status()
                data = response.json()
                routes = data.get('routes', [])
                if routes:
                    distance = routes[0]['distance']  # Distance in meters
                    duration = routes[0]['duration']  # Duration in seconds
                    return distance, duration
                else:
                    return None, None

        distance, duration = asyncio.run(fetch_route())

        return distance, duration
