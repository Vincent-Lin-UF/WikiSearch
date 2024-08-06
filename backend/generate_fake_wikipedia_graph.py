import json
import random
from tqdm import tqdm

def generate_fake_wikipedia_graph(num_nodes=10000, min_links=1, max_links=20):
    graph = {}
    
    titles = [f"Page_{i}" for i in range(num_nodes)]
    
    print("Generating fake Wikipedia graph...")
    for i in tqdm(range(num_nodes)):
        page_id = i
        title = titles[i]
        num_links = random.randint(min_links, min(max_links, num_nodes - 1))
        outgoing_links = random.sample(range(num_nodes), num_links)
        outgoing_links = [link for link in outgoing_links if link != page_id]
        
        graph[page_id] = {
            "id": page_id,
            "title": title,
            "outgoing_links": outgoing_links
        }
    
    return graph

def save_graph_to_json(graph, filename="fake_wikipedia_graph.json"):
    print(f"Saving graph to {filename}...")
    with open(filename, 'w') as f:
        json.dump(graph, f)
    print("Done!")

num_nodes = 10000
graph = generate_fake_wikipedia_graph(num_nodes)
save_graph_to_json(graph)