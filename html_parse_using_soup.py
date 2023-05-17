import pickle
import requests
import spacy

import matplotlib.pyplot as plt
import networkx as nx

from bs4 import BeautifulSoup
from helper import get_articles, get_sentences, extract_subject_object_relationship


nlp = spacy.load("en_core_web_sm")

# variable initialization
entities = []
triple_list = []

# Scraping the articles from the website
url = "https://english.onlinekhabar.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


# Finding all the article links
article_links = [article.find("a")["href"] for article in soup.find_all("li")]

# Scraping the articles from the links
articles = get_articles(article_links)

sentences = get_sentences(articles)


for idx, sent in enumerate(sentences):
    # entities 
    for entity in sent.ents:
        entities.append((entity.text, entity.label_))

    # triples
    triple = extract_subject_object_relationship(sent.text)
    # print(f'triple: {triple}')
    if triple[0] and triple[2]:
        triple_list.append(triple)

# rs = []
# for s, r, o in triple_list:
#     rs.append(r)
# for r in list(set(rs)):
#     print(f'{r} means: {spacy.explain(r)}')

# Generate Directed Graph
G = nx.DiGraph()

for triple in triple_list:
    subject = triple[0]
    obj = triple[2]
    relationship = triple[1]
    G.add_edge(subject, obj, label=relationship)

# Write the Graph into pickle file
with open("knowledge_graph.pickle", 'wb') as f:
    pickle.dump(G, f)
    print("Knowledge graph saved.")

# Load the graph from the pickle file
with open("knowledge_graph.pickle", "rb") as f:
    G = pickle.load(f)
    # print(G)

# Plot the graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)
nx.draw(
    G, 
    pos, 
    with_labels=True, 
    node_color="lightblue", 
    node_size=5, 
    edge_color="gray", 
    arrows=True
)

edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Knowledge Graph")
plt.show()

# Example: Print the number of nodes in the graph
print("Number of nodes:", len(G.nodes))

# Example: Print the number of edges in the graph
print(f"Number of edges: {len(G.edges)}")