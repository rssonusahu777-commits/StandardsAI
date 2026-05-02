import sys
import os

# Ensure backend directory is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from fastapi.testclient import TestClient
from backend.src.main import app

client = TestClient(app)

def run_tests():
    with TestClient(app) as client:
        print("Testing GET /categories...")
        response = client.get("/categories")
        if response.status_code == 200:
            print(f"SUCCESS: /categories returned {response.json()}")
        else:
            print(f"FAILED: /categories returned {response.status_code} - {response.text}")

        print("\nTesting POST /analyze (with auto-detect)...")
        payload = {"query": "I need some portland cement for a building"}
        response = client.post("/analyze", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: /analyze returned {len(data['results'])} results.")
            print(f"First result: {data['results'][0]['standard']} ({data['results'][0]['category']})")
        else:
            print(f"FAILED: /analyze returned {response.status_code} - {response.text}")
            
        print("\nTesting POST /analyze (with strict category filter)...")
        payload = {"query": "I need structural rebars", "category": "steel"}
        response = client.post("/analyze", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: /analyze returned {len(data['results'])} results.")
            for r in data['results']:
                if r['category'] != 'steel':
                     print(f"FAILED: strict filtering failed. Got {r['category']}")
                     return
            print("SUCCESS: Strict filtering verified!")
        else:
            print(f"FAILED: /analyze returned {response.status_code} - {response.text}")

if __name__ == '__main__':
    run_tests()
