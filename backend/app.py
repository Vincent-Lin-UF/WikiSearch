from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from algos.bfs import bfs
from algos.dijkstra import dijkstra
import time

app = Flask(__name__)
CORS(app)

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'dump', 'sdow.sqlite')

def get_db_connection():
    if not os.path.exists(DATABASE_PATH):
        raise FileNotFoundError(f"Database file not found at {DATABASE_PATH}")
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.json
    start = data['start']
    end = data['end']
    algorithm = data['algorithm']
    
    conn = get_db_connection()
    
    # Get page IDs
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
        # Convert page IDs back to titles
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

@app.route('/db_status', methods=['GET'])
def db_status():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Get row counts for each table
        table_counts = {}
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            table_counts[table] = count
        
        conn.close()
        
        return jsonify({
            "status": "connected",
            "database_path": DATABASE_PATH,
            "tables": tables,
            "row_counts": table_counts
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "database_path": DATABASE_PATH
        }), 500

if __name__ == '__main__':
    app.run(debug=True)