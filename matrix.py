import pandas as pd
import numpy as np
from itertools import permutations

# Haversine distance function
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    
    a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = R * c
    return np.round(distance, 2)

# Read input dataset
def read_input_dataset(file_path):
    df = pd.read_csv(file_path)
    return df

# Calculate distances between locations
def calculate_distances(df):
    locations = df[['order_id', 'lat', 'lng']].values
    depot_location = (df['depot_lat'].iloc[0], df['depot_lng'].iloc[0])
    num_locations = len(locations)
    distance_matrix = np.zeros((num_locations + 1, num_locations + 1), dtype=float)  # Initialize distance matrix
    
    for i, location in enumerate(locations):
        order_id, lat, lng = location
        location_coords = (lat, lng)
        distance_to_depot = haversine(lat, lng, depot_location[0], depot_location[1])
        distance_matrix[0, i + 1] = distance_to_depot  # Distance from depot to customer
        distance_matrix[i + 1, 0] = distance_to_depot  # Distance from customer to depot
        
        for j, other_location in enumerate(locations):
            other_order_id, other_lat, other_lng = other_location
            other_location_coords = (other_lat, other_lng)
            distance = haversine(lat, lng, other_lat, other_lng)
            distance_matrix[i + 1, j + 1] = distance
    
    return distance_matrix, df['order_id'].tolist()

# Find optimal route using brute force (permutations)
def find_optimal_route(distance_matrix, order_ids):
    min_distance = float('inf')
    optimal_route = []
    for perm in permutations(range(1, len(order_ids) + 1)):
        route = [0] + list(perm) + [0]  # Include depot at beginning and end of route
        total_distance = calculate_route_distance(route, distance_matrix)
        if total_distance < min_distance:
            min_distance = total_distance
            optimal_route = route
    return optimal_route, min_distance

# Calculate total distance of a route
def calculate_route_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        from_node = route[i]
        to_node = route[i + 1]
        total_distance += distance_matrix[from_node][to_node]
    return total_distance

# Main function
def main():
    input_files = ['part_a_input_dataset_1.csv', 'part_a_input_dataset_2.csv', 'part_a_input_dataset_3.csv', 'part_a_input_dataset_4.csv', 'part_a_input_dataset_5.csv']
    best_routes = {}
    for file_path in input_files:
        df = read_input_dataset(file_path)
        distance_matrix, order_ids = calculate_distances(df)
        optimal_route, min_distance = find_optimal_route(distance_matrix, order_ids)
        best_routes[file_path] = (optimal_route, min_distance)
    # Display the best routes in tabular form
    print("Best routes:")
    print("Input Dataset\tBest Route\tTotal Distance (km)")
    for dataset, (route, total_distance) in best_routes.items():
        print(f"{dataset}\t{route}\t{total_distance:.2f}")

if __name__ == "__main__":
    main()

