from typing import List, Any
import heapq
from models import Priority
from fastapi import HTTPException

def split_batches(ids: List[int], batch_size: int = 3) -> List[List[int]]:
    """Split a list of IDs into batches of specified size."""
    if not ids:
        raise HTTPException(status_code=400, detail="IDs list cannot be empty")
    
    if batch_size < 1:
        raise HTTPException(status_code=400, detail="Batch size must be at least 1")
    
    return [ids[i:i + batch_size] for i in range(0, len(ids), batch_size)]

def enqueue_batches(ingestion_id: str, priority: Priority, batches: List[List[int]], created_at: float, batch_queue: List[Any]) -> None:
    """Enqueue batches with priority and creation time."""
    if not ingestion_id:
        raise HTTPException(status_code=400, detail="Ingestion ID cannot be empty")
    
    if not batches:
        raise HTTPException(status_code=400, detail="Batches list cannot be empty")
    
    if not isinstance(priority, Priority):
        raise HTTPException(status_code=400, detail="Invalid priority value")
    
    priority_value = {
        Priority.HIGH: 0,
        Priority.MEDIUM: 1,
        Priority.LOW: 2
    }
    
    for batch in batches:
        if not batch:
            continue  # Skip empty batches
        # Priority queue entry: (priority_value, created_at, ingestion_id, batch)
        heapq.heappush(batch_queue, (priority_value[priority], created_at, ingestion_id, batch))
