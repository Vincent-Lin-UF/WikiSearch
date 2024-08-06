import requests
import json

def test_find_path(start, end, algorithm):
    url = "http://localhost:5000/find_path"
    payload = {
        "start": start,
        "end": end,
        "algorithm": algorithm
    }
    headers = {"Content-Type": "application/json"}

    print(f"Sending request to: {url}")
    print(f"Payload: {payload}")

    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Raw Response: {response.text}")
    
    try:
        print(f"JSON Response: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print("Response is not valid JSON")

test_find_path("Page_0", "Page_100", "bfs")
test_find_path("Page_0", "Page_100", "dijkstra")