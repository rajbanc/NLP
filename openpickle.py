import pickle
import matplotlib.pyplot as plt
import networkx as nx



with open('Knowledge_graph.pickle','rb') as f:
    G = pickle.load(f)
    print(G)
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=20)

edge_labels = nx.get_edge_attributes(G, "label")
nx.draw(G, pos, with_labels=True, node_color="red", node_size=5, edge_color="gray", arrows=True)

plt.title("Knowledge Graph")
plt.show()