import heapq

def dijkstra(conn, start_id, end_id):
    distances = {start_id: 0}
    previous = {start_id: None}
    pq = [(0, start_id)]
    visited = set()

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_vertex == end_id:
            path = []
            while current_vertex:
                path.append(current_vertex)
                current_vertex = previous[current_vertex]
            return path[::-1], list(visited)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        cursor = conn.cursor()
        cursor.execute('SELECT to_page_id FROM links WHERE from_page_id = ?', (current_vertex,))
        neighbors = cursor.fetchall()

        for neighbor in neighbors:
            neighbor_id = neighbor[0]
            distance = current_distance + 1 

            if neighbor_id not in distances or distance < distances[neighbor_id]:
                distances[neighbor_id] = distance
                previous[neighbor_id] = current_vertex
                heapq.heappush(pq, (distance, neighbor_id))

    return None, list(visited)  # No path found