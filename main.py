from src import Index


origin = (-6.8096036,39.2854829)
destination = (-6.867255,39.310245)

single_target = (-6.7870493, 39.2044721)  # Ubungo Maji, Dar Es Salaam, Tanzania
point_target = (-6.82186645, 39.301757704855774) # Ferry Terminal, Dar Es Salaam, Tanzania



# bearings = Index().get_bearing(origin, destination)
# print("Bearings: ",bearings)



# distance = Index().get_euclidean_distance(origin, destination)
# print("Distance: ",distance)

# distance = Index().get_great_circle_distance(origin, destination)
# print("Great Circle Distance: ",distance)

# coordinates = Index().geocode("Ubungo Maji, Dar Es Salaam, Tanzania")
# print("Coordinates: ",coordinates)


# graph = Index().get_graph("Ubungo Maji, Dar Es Salaam, Tanzania", "drive")
# print("Graph: ",graph)


# distance = Index().get_road_distance("Ubungo Maji, Dar Es Salaam, Tanzania", "Ferry Terminal, Dar Es Salaam, Tanzania", 'drive')
# print("Road Distance: ",distance)

# distance = Index().get_road_distance(origin, destination, mode='drive', weight='time')
# print("Road Distance: ",distance)


# distance matrix

# origins = [origin, single_target]
# destinations = [destination, point_target]

# matrix = Index().get_distance_matrix(origins, destinations, mode='drive', weight='time')
# print("Distance Matrix: ",matrix) 


# # bbox coodinates
# north = -6.6900
# south = -7.2000
# east = 39.3000
# west = 39.7000


# graph = Index().get_graph_from_bbox(north=north, south=south, east=east, west=west, network_type="walk")
    
# # Save the graph
# Index.save_graph(graph, graph_name="dar_es_salaam", network_type="walk")


# graph = Index.load_graph("dar_es_salaam", "walk")

# print(type(graph))
# Index.visualize_network(graph)


start = (6.7924, 39.2083)  # Example coordinates for Dar es Salaam
end = (6.7930, 39.2090)  # Another example coordinate
distance, duration = Index.get_route(origin, destination)

if distance is not None and duration is not None:
    print(f"Distance: {distance} meters")
    print(f"Duration: {duration} seconds")
else:
    print("No route found.")