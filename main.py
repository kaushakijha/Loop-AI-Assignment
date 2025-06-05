from fastapi import FastAPI, HTTPException
from models import IngestRequest
from storage import ingestion_store, create_ingestion_entry, get_ingestion_status, batch_queue
from utils import split_batches, enqueue_batches
from worker import start_worker
import uuid
import time
import heapq

app = FastAPI()
start_worker()
@app.get("/")
def root():
    return {"message": "Ingestion API is live!"}

@app.post("/ingest")
def ingest(request: IngestRequest):
    ingestion_id = str(uuid.uuid4())
    created_at = time.time()

    batches = split_batches(request.ids)
    create_ingestion_entry(ingestion_id, batches)
    enqueue_batches(ingestion_id, request.priority, batches, created_at, batch_queue)

    return {"ingestion_id": ingestion_id}

@app.get("/status/{ingestion_id}")
def status(ingestion_id: str):
    status = get_ingestion_status(ingestion_id)
    if not status:
        raise HTTPException(status_code=404, detail="Ingestion ID not found")
    return {
        "ingestion_id": ingestion_id,
        "status": status["status"],
        "batches": [
            {"batch_id": b["batch_id"], "ids": b["ids"], "status": b["status"]}
            for b in status["batches"]
        ]
    }
