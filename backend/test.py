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

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Raw Response: {response.text}")
    
    try:
        print(f"JSON Response: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print("Response is not valid JSON")

# Test cases
test_find_path("Python (programming language)", "Philosophy", "bfs")