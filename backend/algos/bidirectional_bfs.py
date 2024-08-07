from collections import deque

def bidirectional_bfs(database, start_id, end_id):
    if start_id == end_id:
        return [start_id], {start_id}

    forward_queue = deque([(start_id, [start_id])])
    backward_queue = deque([(end_id, [end_id])])
    forward_visited = {start_id: [start_id]}
    backward_visited = {end_id: [end_id]}

    while forward_queue and backward_queue:
        #forawrd
        current, path = forward_queue.popleft()
        for neighbor in database.fetch_outgoing_links(current):
            if neighbor in backward_visited:
                return path + backward_visited[neighbor][::-1][1:], set(forward_visited) | set(backward_visited)
            if neighbor not in forward_visited:
                forward_visited[neighbor] = path + [neighbor]
                forward_queue.append((neighbor, path + [neighbor]))

        #backwards
        current, path = backward_queue.popleft()
        for neighbor in database.fetch_outgoing_links(current):
            if neighbor in forward_visited:
                return forward_visited[neighbor] + path[::-1][1:], set(forward_visited) | set(backward_visited)
            if neighbor not in backward_visited:
                backward_visited[neighbor] = [neighbor] + path
                backward_queue.append((neighbor, [neighbor] + path))

    return None, set(forward_visited) | set(backward_visited)