import heapq
from typing import Dict, List, Any
import uuid
import time

# In-memory storage for ingestion status
ingestion_store: Dict[str, Dict[str, Any]] = {}

# Priority queue for batches
batch_queue = []

def create_ingestion_entry(ingestion_id: str, batches: List[List[int]]) -> None:
    """Create a new ingestion entry with initial status."""
    ingestion_store[ingestion_id] = {
        "status": "yet_to_start",
        "batches": [
            {
                "batch_id": str(uuid.uuid4()),
                "ids": batch,
                "status": "yet_to_start",
                "created_at": time.time()
            }
            for batch in batches
        ],
        "created_at": time.time()
    }

def get_ingestion_status(ingestion_id: str) -> Dict[str, Any]:
    """Get the current status of an ingestion request."""
    return ingestion_store.get(ingestion_id)

def update_batch_status(ingestion_id: str, batch_id: str, status: str) -> None:
    """Update the status of a specific batch."""
    if ingestion_id in ingestion_store:
        for batch in ingestion_store[ingestion_id]["batches"]:
            if batch["batch_id"] == batch_id:
                batch["status"] = status
                break
        
        # Update overall status
        batch_statuses = [b["status"] for b in ingestion_store[ingestion_id]["batches"]]
        if all(status == "completed" for status in batch_statuses):
            ingestion_store[ingestion_id]["status"] = "completed"
        elif any(status == "triggered" for status in batch_statuses):
            ingestion_store[ingestion_id]["status"] = "triggered"
        else:
            ingestion_store[ingestion_id]["status"] = "yet_to_start"
