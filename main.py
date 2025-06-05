from fastapi import FastAPI, HTTPException
from models import IngestRequest, Priority
from storage import ingestion_store, create_ingestion_entry, get_ingestion_status, batch_queue
from utils import split_batches, enqueue_batches
from worker import start_worker
import uuid
import time
import heapq
from typing import List, Dict
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

app = FastAPI()
start_worker()

@app.get("/")
def root():
    return {"message": "Ingestion API is live!"}

@app.post("/ingest")
async def ingest(request: IngestRequest):
    try:
        ingestion_id = str(uuid.uuid4())
        created_at = time.time()

        batches = split_batches(request.ids)
        create_ingestion_entry(ingestion_id, batches)
        enqueue_batches(ingestion_id, request.priority, batches, created_at, batch_queue)

        return {"ingestion_id": ingestion_id}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{ingestion_id}")
async def status(ingestion_id: str) -> Dict:
    try:
        status_data = get_ingestion_status(ingestion_id)
        if not status_data:
            raise HTTPException(status_code=404, detail="Ingestion ID not found")
        
        return {
            "ingestion_id": ingestion_id,
            "status": status_data["status"],
            "batches": [
                {
                    "batch_id": batch["batch_id"],
                    "ids": batch["ids"],
                    "status": batch["status"]
                }
                for batch in status_data["batches"]
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for err in exc.errors():
        if err["type"] == "int_parsing":
            errors.append({
                "type": "validation_error",
                "loc": err["loc"],
                "msg": "ID must be an integer between 1 and 10^9+7",
                "input": err["input"]
            })
        elif err["type"] == "enum":
            errors.append({
                "type": "validation_error",
                "loc": err["loc"],
                "msg": f"Priority must be one of {[p.value for p in Priority]}",
                "input": err["input"]
            })
        else:
            errors.append({
                "type": "validation_error",
                "loc": err["loc"],
                "msg": err["msg"],
                "input": err["input"]
            })
    
    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )
