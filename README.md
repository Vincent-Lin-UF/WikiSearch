# WikiSearch

This projects uses BFS, Djikstra's, Bellman-Ford, and Bi-Directional BFS shortest path finding algorithm to find the shortest path between two wikipedia pages

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+

## Setup

### Backend

1. Navigate to the backend directory:
```
cd backend
```

2. Create a virtual environment:
```
python -m venv env
```

3. Activate the virtual environment:
- On Windows:
  ```
  .\env\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source env/bin/activate
  ```

4. Install the required Python packages:
```
pip install -r requirements.txt
```

5. Generate the fake Wikipedia graph:
```
python generate_fake_graph.py
```

### Frontend

1. Navigate to the frontend directory:
```
cd frontend
```

2. Install the required npm packages:
```
npm install
```

## Running the Application

### Backend

1. From the backend directory, start the Flask server:
```
python app.py
```

The server will start running on `http://localhost:5000`.

### Frontend

1. From the frontend directory, start the React server:
```
npm start
```

The application will open in your default web browser at `http://localhost:3000`.

## Using the Application

1. In the web interface, you'll see two input fields: "Start Page" and "End Page".

3. Type a start page and an end page from the suggestions. Example "Page_12" and "Page_2342".

4. Click either the "Find Path (BFS)", "Find Path (Dijkstra), "Find Path (Bellman-Ford)", or "Find Path (Bi-BFS)" button to find the shortest path between the two pages using the selected algorithm.

5. The results will display the path found, the number of pages visited during the search, and the time taken to find the path.

## Project Structure

- `backend/`: Contains the Flask server and Search algorithms.
- `app.py`: The main Flask app.
- `database.py`: Handles interactions with the fake Wikipedia graph.
- `algos/`: Contains the BFS, Dijkstra, Bellman-Ford, and Bi-Directional Search algorithms.
- `generate_fake_graph.py`: Script to generate the fake Wikipedia graph.
- `noWork/`: [No longer used] Contains the old `database.py` used for the acutal wikipedia database.
- `scripts/`: [No longer used] Contains all the scripts to extract, process, and refine the wikipedia database onto an adjacency list of SQL tables.
- `sql/`: [No longer used] Contains all the instructions to create the SQL tables.
- `test.py`: Used to test the backend without needing the frontend.

- `frontend/`: Contains the React application.
- `src/`: Source files for the React app.
 - `App.js`: The main React component.
 - `WikiSearch.js`: The component for the pathfinding interface.

 ## Connect on LinkedIn!

 Vincent Lin - https://www.linkedin.com/in/vincent-lin-uf/
