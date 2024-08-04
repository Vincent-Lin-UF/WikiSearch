from collections import deque

def bfs(conn, start_id, end_id):
    queue = deque([(start_id, [start_id])])
    visited = set([start_id])

    while queue:
        (vertex, path) = queue.popleft()
        if vertex == end_id:
            return path, list(visited)

        cursor = conn.cursor()
        cursor.execute('SELECT to_page_id FROM links WHERE from_page_id = ?', (vertex,))
        neighbors = cursor.fetchall()

        for neighbor in neighbors:
            neighbor_id = neighbor[0]
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append((neighbor_id, path + [neighbor_id]))

    return None, list(visited)