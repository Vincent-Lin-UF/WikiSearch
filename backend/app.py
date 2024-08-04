from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from algorithms.bfs import bfs
from algorithms.dijkstra import dijkstra
import time

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('wikipedia.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.json
    start = data['start']
    end = data['end']
    algorithm = data['algorithm']
    
    conn = get_db_connection()
    
    # getting the page ids
    start_id = conn.execute('SELECT id FROM pages WHERE title = ?', (start,)).fetchone()
    end_id = conn.execute('SELECT id FROM pages WHERE title = ?', (end,)).fetchone()
    
    if not start_id or not end_id:
        conn.close()
        return jsonify({'error': 'Start or end page not found'}), 404
    
    start_time = time.time()
    
    if algorithm == 'bfs':
        path, visited = bfs(conn, start_id['id'], end_id['id'])
    elif algorithm == 'dijkstra':
        path, visited = dijkstra(conn, start_id['id'], end_id['id'])
    else:
        conn.close()
        return jsonify({'error': 'Invalid algorithm'}), 400
    
    end_time = time.time()
    
    conn.close()
    
    if path:
        # putting the page id back to the titles
        path_titles = get_titles_from_ids(path)
        visited_titles = get_titles_from_ids(visited)
        return jsonify({
            'path': path_titles,
            'visited': visited_titles,
            'time_taken': end_time - start_time
        })
    else:
        return jsonify({'error': 'No path found'}), 404

def get_titles_from_ids(ids):
    conn = get_db_connection()
    titles = []
    for id in ids:
        title = conn.execute('SELECT title FROM pages WHERE id = ?', (id,)).fetchone()
        if title:
            titles.append(title['title'])
    conn.close()
    return titles

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '')
    conn = get_db_connection()
    results = conn.execute('SELECT title FROM pages WHERE title LIKE ? LIMIT 10', (f'{query}%',)).fetchall()
    conn.close()
    return jsonify([result['title'] for result in results])

if __name__ == '__main__':
    app.run(debug=True)