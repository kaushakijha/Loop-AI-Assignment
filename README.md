# Data Ingestion API System

A FastAPI-based system for handling data ingestion requests with priority-based processing and rate limiting.

## Features

- RESTful API endpoints for data ingestion and status checking
- Priority-based batch processing (HIGH, MEDIUM, LOW)
- Rate limiting (1 batch per 5 seconds)
- Asynchronous processing with background worker
- In-memory storage for request tracking

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Ingest Data

- **Endpoint**: POST /ingest
- **Input**:

```json
{
  "ids": [1, 2, 3, 4, 5],
  "priority": "HIGH"
}
```

- **Output**:

```json
{
  "ingestion_id": "abc123"
}
```

### 2. Check Status

- **Endpoint**: GET /status/{ingestion_id}
- **Output**:

```json
{
  "ingestion_id": "abc123",
  "status": "triggered",
  "batches": [
    {
      "batch_id": "uuid",
      "ids": [1, 2, 3],
      "status": "completed"
    },
    {
      "batch_id": "uuid",
      "ids": [4, 5],
      "status": "triggered"
    }
  ]
}
```

## Implementation Details

- Uses FastAPI for the REST API
- Implements priority queue for batch processing
- Enforces rate limiting of 1 batch per 5 seconds
- Processes IDs in batches of 3
- Simulates external API calls with delays
- Maintains status tracking for each batch and overall ingestion

## Status Values

### Batch Status

- yet_to_start
- triggered
- completed

### Overall Status

- yet_to_start (all batches yet to start)
- triggered (at least one batch triggered)
- completed (all batches completed)
