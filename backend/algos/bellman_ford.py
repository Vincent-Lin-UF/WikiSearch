def bellman_ford(database, start_id, end_id):
    distances = {page_id: float('inf') for page_id in range(len(database.graph))}
    distances[start_id] = 0
    predecessors = {page_id: None for page_id in range(len(database.graph))}
    
    visited = set()

    for _ in range(len(database.graph) - 1):
        updated = False
        for page_id in range(len(database.graph)):
            if distances[page_id] != float('inf'):
                visited.add(page_id)
                for neighbor in database.fetch_outgoing_links(page_id):
                    if distances[page_id] + 1 < distances[neighbor]:
                        distances[neighbor] = distances[page_id] + 1
                        predecessors[neighbor] = page_id
                        updated = True
                        
                        if neighbor == end_id:
                            path = []
                            current = end_id
                            while current is not None:
                                path.append(current)
                                current = predecessors[current]
                            return path[::-1], list(visited)
        
        if not updated:
            break

    return None, list(visited)