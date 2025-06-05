from typing import List, Any
import heapq
from models import Priority

def split_batches(ids: List[int], batch_size: int = 3) -> List[List[int]]:
    """Split a list of IDs into batches of specified size."""
    return [ids[i:i + batch_size] for i in range(0, len(ids), batch_size)]

def enqueue_batches(ingestion_id: str, priority: Priority, batches: List[List[int]], created_at: float, batch_queue: List[Any]) -> None:
    """Enqueue batches with priority and creation time."""
    priority_value = {
        Priority.HIGH: 0,
        Priority.MEDIUM: 1,
        Priority.LOW: 2
    }
    
    for batch in batches:
        # Priority queue entry: (priority_value, created_at, ingestion_id, batch)
        heapq.heappush(batch_queue, (priority_value[priority], created_at, ingestion_id, batch))
