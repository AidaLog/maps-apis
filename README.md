# MAPS API

(mostly experimental)

## Target Features

| Feature                               | Description                                                                                                                                                                                                                                                          |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Geocoding                            | Convert addresses into geographic coordinates (latitude and longitude), enabling applications to find locations or display addresses on maps.                                                                                                                     |
| Reverse Geocoding                    | Convert geographic coordinates (latitude and longitude) into addresses, allowing applications to determine the location of a point on a map based on its coordinates.                                                                                                |
| Routing and Directions               | Provide reliable routing and direction services for different modes of transportation (e.g., driving, walking, public transit) with real-time traffic updates, helping users navigate from one location to another efficiently.                                    |
| Place Search and Recommendations    | Enable users to search for places of interest (e.g., restaurants, hotels, attractions) and receive personalized recommendations based on their preferences and current location, enhancing the discovery of nearby businesses and attractions.                        |
| Distance Matrix                     | Calculate travel distance and time for a matrix of origins and destinations, providing users with the ability to determine the best route for multiple locations and optimize travel plans.                                                                          |

## Usage

### 1. Creating an Instance of the Index Class

First, you need to create an instance of the `Index` class:

```python
index = Index()
```

### 2. Calculating Bearing Between Two Points

To calculate the bearing between two latitude-longitude points, you can use the `get_bearing` method:

```python
origin = (37.7749, -122.4194)
destination = (34.0522, -118.2437)
bearing = index.get_bearing(origin, destination)
print("Bearing:", bearing)
```

### 3. Calculating Distance Between Two Points

You can calculate the distance between two points using either Euclidean distance or great-circle distance:

```python
# Euclidean distance
euclidean_distance = index.get_distance(origin, destination, kind='euclidean')
print("Euclidean Distance:", euclidean_distance)

# Great-circle distance
great_circle_distance = index.get_distance(origin, destination, kind='great_circle')
print("Great Circle Distance:", great_circle_distance)
```

### 4. Finding the Center Point

To find the center point between two lat-long points, use the `get_center` method:

```python
center_point = index.get_center(origin, destination)
print("Center Point:", center_point)
```

### 5. Geocoding a Place Name

You can obtain the latitude and longitude of a place name using the `geocode` method:

```python
place_name = 'Los Angeles, California'
location = index.geocode(place_name)
print("Location:", location)
```

### 6. Retrieving Street Network Graph

To retrieve the street network graph for a place, use the `get_graph` method:

```python
place_name = 'Los Angeles, California'
network_type = 'drive'  # Options: 'drive', 'walk', 'bike', 'all'
graph = index.get_graph(place_name, network_type)
print("Street Network Graph:", graph)
```

### 7. Finding Shortest Route

To find the shortest route between two points on the street network, use the `get_shortest_route` method:

```python
origin = (37.7749, -122.4194)
destination = (34.0522, -118.2437)
mode = 'drive'  # Options: 'drive', 'walk', 'bike', 'all'
weight = 'length'  # Options: 'time', 'length', 'cost', 'speed', 'elevation'
route = index.get_shortest_route(origin, destination, mode, weight)
print("Shortest Route:", route)
```

### 8. Calculating Road Distance

You can calculate the road distance between two points by following the roads using the `get_road_distance` method:

```python
origin = (37.7749, -122.4194)
destination = (34.0522, -118.2437)
mode = 'drive'  # Options: 'drive', 'walk', 'bike', 'all'
weight = 'length'  # Options: 'time', 'length', 'cost', 'speed', 'elevation'
road_distance = index.get_road_distance(origin, destination, mode, weight)
print("Road Distance:", road_distance)
```