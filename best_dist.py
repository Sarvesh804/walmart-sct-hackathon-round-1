import pandas as pd

# Read distance matrix from each dataset file
def read_distance_matrix(file_path):
    df = pd.read_csv(file_path)
    distance_matrix = {}
    for _, row in df.iterrows():
        from_node, to_node, distance = row['From'], row['To'], row['Distance']
        distance_matrix[(from_node, to_node)] = distance
        distance_matrix[(to_node, from_node)] = distance  # Add reverse edge for undirected graph
    return distance_matrix

# Nearest Neighbor Algorithm to find the best delivery route
def nearest_neighbor(distance_matrix):
    nodes = set()
    for (from_node, to_node), distance in distance_matrix.items():
        nodes.add(from_node)
        nodes.add(to_node)
    nodes.remove('Customer 0')  # Remove the depot from the set of nodes
    current_node = 'Customer 0'
    route = [current_node]
    while nodes:
        nearest_node = min(nodes, key=lambda node: distance_matrix.get((current_node, node), float('inf')))
        route.append(nearest_node)
        nodes.remove(nearest_node)
        current_node = nearest_node
    route.append('Customer 0')  # Return to the depot to complete the route
    return route

# Main function
def main():
    file_paths = ['part_a_output_dataset_1_distances.csv', 'part_a_output_dataset_2_distances.csv', 'part_a_output_dataset_3_distances.csv', 'part_a_output_dataset_4_distances.csv', 'part_a_output_dataset_5_distances.csv']
    best_routes = {}
    for i, file_path in enumerate(file_paths, start=1):
        distance_matrix = read_distance_matrix(file_path)
        route = nearest_neighbor(distance_matrix)
        best_routes[f'Dataset {i}'] = route
    # Display the best routes in tabular form
    print("Best routes:")
    for dataset, route in best_routes.items():
        print(f"{dataset}:", " -> ".join(route))

if __name__ == "__main__":
    main()
