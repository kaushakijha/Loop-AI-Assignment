import threading
import time
import heapq
from storage import ingestion_store, batch_queue, update_batch_status
from typing import List, Any
import asyncio

def mock_fetch_data(id):
    time.sleep(1)  # Simulate external API delay
    return {"id": id, "data": "processed"}

async def process_batch(ingestion_id: str, batch: List[int]) -> None:
    """Process a single batch of IDs."""
    # Simulate external API call with delay
    await asyncio.sleep(1)  # Simulate API call delay
    return {"id": batch, "data": "processed"}

async def worker_loop() -> None:
    """Main worker loop that processes batches from the queue."""
    while True:
        if not batch_queue:
            await asyncio.sleep(0.1)
            continue

        # Get the highest priority batch
        priority, created_at, ingestion_id, batch = batch_queue[0]
        
        # Find the correct batch_id from ingestion_store
        batch_id = None
        for b in ingestion_store[ingestion_id]["batches"]:
            if b["ids"] == batch:
                batch_id = b["batch_id"]
                break

        if batch_id is None:
            heapq.heappop(batch_queue)  # Remove invalid batch
            continue

        # Check if we need to wait for rate limit
        current_time = time.time()
        if current_time - created_at < 5:
            await asyncio.sleep(5 - (current_time - created_at))
        
        # Process the batch
        update_batch_status(ingestion_id, batch_id, "triggered")
        await process_batch(ingestion_id, batch)
        update_batch_status(ingestion_id, batch_id, "completed")
        
        # Remove the processed batch from queue
        heapq.heappop(batch_queue)

def start_worker() -> None:
    """Start the background worker thread."""
    def run_worker():
        asyncio.run(worker_loop())
    
    worker_thread = threading.Thread(target=run_worker, daemon=True)
    worker_thread.start()
