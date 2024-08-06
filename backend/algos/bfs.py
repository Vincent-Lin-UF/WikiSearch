import logging
from collections import deque

def bfs(database, start_id, end_id):
    queue = deque([(start_id, [start_id])])
    visited = set([start_id])

    while queue:
        (vertex, path) = queue.popleft()
        if vertex == end_id:
            return path, list(visited)

        neighbors = database.fetch_outgoing_links(vertex)

        for neighbor_id in neighbors:
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append((neighbor_id, path + [neighbor_id]))

    return None, list(visited)  # No path found