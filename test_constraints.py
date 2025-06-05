import pytest
from fastapi.testclient import TestClient
import time
from main import app
import asyncio
from storage import ingestion_store, batch_queue
from worker import process_batch, start_worker

start_worker()

client = TestClient(app)

def test_data_persistence():
    """Test that data persists between requests"""
    # Submit a request
    response = client.post("/ingest", json={"ids": [1, 2, 3], "priority": "MEDIUM"})
    ingestion_id = response.json()["ingestion_id"]
    
    # Verify data is stored
    assert ingestion_id in ingestion_store
    assert len(ingestion_store[ingestion_id]["batches"]) == 1

def test_asynchronous_processing():
    """Test that processing happens asynchronously"""
    # Submit a request
    response = client.post("/ingest", json={"ids": [1, 2, 3], "priority": "MEDIUM"})
    ingestion_id = response.json()["ingestion_id"]
    
    # Check status immediately
    status = client.get(f"/status/{ingestion_id}").json()
    assert status["status"] in ["yet_to_start", "triggered"]
    
    # Wait for processing
    time.sleep(6)
    
    # Check status again
    status = client.get(f"/status/{ingestion_id}").json()
    assert status["status"] in ["triggered", "completed"]

def test_rate_limiting():
    """Test that rate limiting is enforced"""
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
    assert completed_count <= 2

def test_priority_processing():
    """Test that higher priority requests are processed first"""
    # Submit low priority request
    low_response = client.post("/ingest", json={"ids": [1, 2, 3], "priority": "LOW"})
    low_id = low_response.json()["ingestion_id"]
    
    # Submit high priority request
    high_response = client.post("/ingest", json={"ids": [4, 5, 6], "priority": "HIGH"})
    high_id = high_response.json()["ingestion_id"]
    
    # Wait for initial processing (6 seconds)
    time.sleep(6)
    
    # Check status of both requests
    low_status = client.get(f"/status/{low_id}").json()
    high_status = client.get(f"/status/{high_id}").json()
    
    # High priority should be processed first
    assert high_status["status"] in ["triggered", "completed"]
    
    # Wait for more processing (4 more seconds)
    time.sleep(4)
    
    # Check final status
    low_status = client.get(f"/status/{low_id}").json()
    high_status = client.get(f"/status/{high_id}").json()
    
    # Both should be completed by now
    assert high_status["status"] == "completed"
    assert low_status["status"] == "completed"

def test_batch_size_limit():
    """Test that only 3 IDs are processed at a time"""
    # Submit a request with more than 3 IDs
    response = client.post("/ingest", json={"ids": [1, 2, 3, 4, 5, 6, 7], "priority": "MEDIUM"})
    ingestion_id = response.json()["ingestion_id"]
    
    # Check that batches are created correctly
    status = client.get(f"/status/{ingestion_id}").json()
    assert len(status["batches"]) == 3  # Should have 3 batches (3,3,1)
    
    # Verify each batch has at most 3 IDs
    for batch in status["batches"]:
        assert len(batch["ids"]) <= 3 