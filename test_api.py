import pytest
from fastapi.testclient import TestClient
import time
from main import app

client = TestClient(app)

def test_ingest_endpoint():
    # Test basic ingestion
    response = client.post("/ingest", json={"ids": [1, 2, 3, 4, 5], "priority": "MEDIUM"})
    assert response.status_code == 200
    assert "ingestion_id" in response.json()
    ingestion_id = response.json()["ingestion_id"]

    # Test status endpoint
    response = client.get(f"/status/{ingestion_id}")
    assert response.status_code == 200
    assert response.json()["ingestion_id"] == ingestion_id
    assert response.json()["status"] in ["yet_to_start", "triggered", "completed"]
    assert len(response.json()["batches"]) == 2  # Should have 2 batches (3,2)

def test_priority_processing():
    # Submit low priority request
    low_response = client.post("/ingest", json={"ids": [1, 2, 3], "priority": "LOW"})
    low_id = low_response.json()["ingestion_id"]
    
    # Submit high priority request
    high_response = client.post("/ingest", json={"ids": [4, 5, 6], "priority": "HIGH"})
    high_id = high_response.json()["ingestion_id"]
    
    # Wait for some processing
    time.sleep(6)
    
    # Check status of both requests
    low_status = client.get(f"/status/{low_id}").json()
    high_status = client.get(f"/status/{high_id}").json()
    
    # High priority should be processed first
    assert high_status["status"] in ["triggered", "completed"]
    assert low_status["status"] == "yet_to_start"

def test_rate_limiting():
    # Submit multiple requests
    responses = []
    for i in range(3):
        response = client.post("/ingest", json={"ids": [i*3+1, i*3+2, i*3+3], "priority": "MEDIUM"})
        responses.append(response.json()["ingestion_id"])
    
    # Wait for processing
    time.sleep(6)
    
    # Check status of all requests
    statuses = [client.get(f"/status/{id}").json() for id in responses]
    
    # Only one batch should be processed within 5 seconds
    completed_count = sum(1 for status in statuses if status["status"] == "completed")
    assert completed_count <= 1

def test_invalid_input():
    # Test invalid priority
    response = client.post("/ingest", json={"ids": [1, 2, 3], "priority": "INVALID"})
    assert response.status_code == 422
    
    # Test invalid ID range
    response = client.post("/ingest", json={"ids": [1, 2, 10**9 + 8], "priority": "MEDIUM"})
    assert response.status_code == 422

def test_nonexistent_ingestion_id():
    response = client.get("/status/nonexistent")
    assert response.status_code == 404
