import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Read distances from the output file and build the graph
def build_graph_from_output(file_path):
    # Read the output file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Create an empty graph
    delivery_graph = nx.Graph()
    
    # Add edges to the graph
    for _, row in df.iterrows():
        from_node = row['From']
        to_node = row['To']
        distance = row['Distance']
        delivery_graph.add_edge(from_node, to_node, weight=distance)
    
    return delivery_graph

# Example usage
file_path = 'part_a_output_dataset_1_distances.csv'
delivery_graph = build_graph_from_output(file_path)

# Visualize the graph
plt.figure(figsize=(10, 6))
nx.draw(delivery_graph, with_labels=True, node_size=500, node_color='skyblue', font_size=12, font_weight='bold')
edge_labels = nx.get_edge_attributes(delivery_graph, 'weight')
nx.draw_networkx_edge_labels(delivery_graph, pos=nx.spring_layout(delivery_graph), edge_labels=edge_labels)
plt.title('Delivery Network Graph')
plt.show()
