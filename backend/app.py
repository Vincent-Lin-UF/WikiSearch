from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import logging
from database import Database
from algos.bfs import bfs
from algos.dijkstra import dijkstra

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

# BUCKET_NAME = "cop3530-wiki-data"
# BLOB_NAME = "dumps/20240801/sdow.sqlite.gz"
JSON_FILE_PATH = "fake_wikipedia_graph.json"

try:
    database = Database(JSON_FILE_PATH)
except Exception as e:
    logging.error(f"Failed to initialize database: {str(e)}")
    database = None

@app.route('/find_path', methods=['POST'])
def find_path():
    if database is None:
        return jsonify({'error': 'Database not initialized'}), 500

    data = request.json
    start = data['start']
    end = data['end']
    algorithm = data['algorithm']
    
    logging.info(f"Received request: start={start}, end={end}, algorithm={algorithm}")
    
    try:
        start_id, start_title, is_start_redirect = database.fetch_page(start)
        end_id, end_title, is_end_redirect = database.fetch_page(end)
        logging.info(f"Start ID: {start_id}, End ID: {end_id}")
    except ValueError as e:
        logging.error(f"Error fetching pages: {str(e)}")
        return jsonify({'error': str(e)}), 404
    
    start_time = time.time()
    
    if algorithm == 'bfs':
        path, visited = bfs(database, start_id, end_id)
    elif algorithm == 'dijkstra':
        path, visited = dijkstra(database, start_id, end_id)
    else:
        return jsonify({'error': 'Invalid algorithm'}), 400
    
    end_time = time.time()
    
    if path:
        path_titles = [database.fetch_page(page_id)[1] for page_id in path]
        response = {
            'path': path_titles,
            'visited': len(visited),
            'time_taken': end_time - start_time,
            'is_start_redirect': is_start_redirect,
            'is_end_redirect': is_end_redirect
        }
        logging.info(f"Path found: {response}")
        return jsonify(response)
    else:
        logging.info(f"No path found. Visited {len(visited)} pages.")
        return jsonify({'error': 'No path found'}), 404

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '')
    results = database.autocomplete(query)
    return jsonify(results)

@app.route('/database_status', methods=['GET'])
def database_status():
    try:
        status = database.get_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Test successful"}), 200

if __name__ == '__main__':
    app.run(debug=True)