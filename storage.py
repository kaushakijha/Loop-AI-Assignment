import heapq
from typing import Dict, List, Any
import uuid
import time
from models import Priority

# In-memory storage for ingestion status
ingestion_store: Dict[str, Dict] = {}

# Priority queue for batches
batch_queue: List[Any] = []

def create_ingestion_entry(ingestion_id: str, batches: List[List[int]]) -> None:
    """Create a new ingestion entry with batches."""
    batch_entries = []
    for batch in batches:
        batch_id = str(uuid.uuid4())  # Generate UUID for each batch
        batch_entries.append({
            "batch_id": batch_id,
            "ids": batch,
            "status": "yet_to_start"
        })
    
    ingestion_store[ingestion_id] = {
        "status": "yet_to_start",
        "batches": batch_entries
    }

def get_ingestion_status(ingestion_id: str) -> Dict:
    """Get the current status of an ingestion request."""
    return ingestion_store.get(ingestion_id)

def update_batch_status(ingestion_id: str, batch_id: str, status: str) -> None:
    """Update the status of a specific batch."""
    if ingestion_id not in ingestion_store:
        return
    
    for batch in ingestion_store[ingestion_id]["batches"]:
        if batch["batch_id"] == batch_id:
            batch["status"] = status
            break
    
    # Update overall status
    all_completed = all(b["status"] == "completed" for b in ingestion_store[ingestion_id]["batches"])
    any_triggered = any(b["status"] == "triggered" for b in ingestion_store[ingestion_id]["batches"])
    
    if all_completed:
        ingestion_store[ingestion_id]["status"] = "completed"
    elif any_triggered:
        ingestion_store[ingestion_id]["status"] = "triggered"
    else:
        ingestion_store[ingestion_id]["status"] = "yet_to_start"
