# Data Ingestion API System

## 📁 Project Structure

```
project-root/
│
├── main.py              # FastAPI app
├── models.py            # Pydantic models
├── storage.py           # In-memory data + queue
├── utils.py             # Helper functions
├── worker.py            # Background processing
├── test_constraints.py  # Test suite
├── requirements.txt
└── README.md
```

## 🧠 Brief Explanation of Approach

- **FastAPI** is used to build a modern, high-performance RESTful API for data ingestion and status checking.
- **Pydantic models** ensure strict validation of input data, including ID type/range and priority enum.
- **In-memory storage** (Python dicts and lists) is used for fast, simple, and testable state management.
- **Batching**: IDs are split into batches of up to 3 for rate-limited processing.
- **Priority queue**: Batches are enqueued with priority (HIGH, MEDIUM, LOW) and processed in order.
- **Background worker**: A separate thread asynchronously processes batches, respecting the 5-second rate limit.
- **Status tracking**: Each batch and the overall ingestion request have real-time status updates (`yet_to_start`, `triggered`, `completed`).
- **Comprehensive testing**: All technical constraints and edge cases are covered in the test suite.
- **Clear error handling**: All validation and runtime errors return informative, structured responses.

A robust RESTful API system for handling data ingestion requests with priority-based processing, rate limiting, and batch processing capabilities.

## 🚀 Features

- **Asynchronous Processing**: All ingestion requests are processed asynchronously
- **Priority-based Processing**: Supports HIGH, MEDIUM, and LOW priority levels
- **Rate Limiting**: Enforces a 5-second delay between batch processing
- **Batch Processing**: Automatically splits large requests into batches of 3 IDs
- **In-Memory Storage**: Efficient storage of ingestion requests and their status
- **Status Tracking**: Real-time status updates for each batch and overall ingestion

## 📋 Running Steps

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start the Server

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### Step 5: Verify the Setup

1. Open your browser and visit `http://localhost:8000`

   - You should see: `{"message": "Ingestion API is live!"}`

2. Test the API using curl or Postman:

```bash
# Test the ingest endpoint
curl -X POST "http://localhost:8000/ingest" \
     -H "Content-Type: application/json" \
     -d '{"ids": [1, 2, 3], "priority": "HIGH"}'

# The response will contain an ingestion_id
```

### Step 6: Run Tests

```bash
# Run all tests
pytest test_constraints.py -v

# Run specific test
pytest test_constraints.py::test_priority_processing -v
```

### Step 7: Monitor the Application

- Watch the console for server logs
- Check the status of your ingestion requests
- Monitor the worker processing batches

### Step 8: Stop the Server

- Press `Ctrl+C` in the terminal to stop the server
- Deactivate virtual environment (if used):

```bash
deactivate
```

## 🧪 Testing

To run the full test suite and verify all constraints:

```bash
pytest test_constraints.py -v
```
Screenshot 2025-06-05 114725.png
- This will run all tests and show detailed output for each test case.
- Make sure the server is **not running** when you run the tests (the test client starts its own instance).

## 🛠️ Technical Implementation

### 1. API Endpoints


#### POST /ingest
![image](https://github.com/user-attachments/assets/0757c77e-28df-497b-8b72-4829be431e34)


- Accepts JSON payload with `ids` (list of integers) and `priority` (HIGH/MEDIUM/LOW)
- Returns a unique `ingestion_id` for tracking
- Automatically splits IDs into batches of 3

#### GET /status/{ingestion_id}
![image](https://github.com/user-attachments/assets/e13d13e0-2466-493c-86aa-6c5fdceff790)


- Returns current status of the ingestion request
- Includes overall status and individual batch statuses
- Status values: "yet_to_start", "triggered", "completed"

### 2. Core Components

#### Storage (`storage.py`)

- In-memory storage using dictionaries
- Priority queue for batch processing
- Status tracking for batches and ingestion requests

#### Worker (`worker.py`)

- Background worker thread for processing batches
- Implements rate limiting (5-second delay)
- Handles priority-based processing
- Asynchronous batch processing

#### Utils (`utils.py`)

- Batch splitting logic
- Queue management
- Priority handling

### 3. Testing

Comprehensive test suite covering all technical constraints:
![image](https://github.com/user-attachments/assets/0ba85097-7c47-4541-ba66-40dc3934ffcc)
![image](https://github.com/user-attachments/assets/bfd4f938-7197-4126-ab0b-82c68d476d34)


1. **Data Persistence Test**

   - Verifies data storage between requests
   - Confirms batch creation and storage

2. **Asynchronous Processing Test**

   - Validates non-blocking request handling
   - Confirms status updates during processing

3. **Rate Limiting Test**

   - Ensures 5-second delay between batch processing
   - Verifies rate limit compliance

4. **Priority Processing Test**

   - Confirms HIGH priority requests are processed first
   - Validates priority queue ordering

5. **Batch Size Limit Test**
   - Verifies maximum batch size of 3 IDs
   - Confirms correct batch splitting

## 🔧 Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'fastapi'**

   ```bash
   pip install fastapi uvicorn
   ```

2. **ModuleNotFoundError: No module named 'pytest'**

   ```bash
   pip install pytest
   ```

3. **Application won't start with `python main.py`**

   - This is expected! The application must be run using `uvicorn`
   - FastAPI applications require an ASGI server like uvicorn to run

4. **Port 8000 already in use**
   ```bash
   uvicorn main:app --reload --port 8001
   ```

### Required Dependencies

Make sure you have all these installed:

```bash
pip install fastapi uvicorn pytest httpx
```

## 📊 Test Results

All tests passing successfully:

```
test_data_persistence PASSED
test_asynchronous_processing PASSED
test_rate_limiting PASSED
test_priority_processing PASSED
test_batch_size_limit PASSED
```

## 🔧 Technical Constraints Met

- ✅ FastAPI framework
- ✅ In-memory storage
- ✅ Asynchronous processing
- ✅ Rate limiting (5-second delay)
- ✅ Priority-based processing
- ✅ Batch size limit (3 IDs)
- ✅ Status tracking
- ✅ Error handling

## 📝 API Usage Examples

### Using Postman

1. **Submit an Ingestion Request**

   - Method: `POST`
   - URL: `http://localhost:8000/ingest`
   - Headers:
     ```
     Content-Type: application/json
     ```
   - Body (raw JSON):
     ```json
     {
       "ids": [1, 2, 3, 4, 5],
       "priority": "HIGH"
     }
     ```
   - Valid priority values: "HIGH", "MEDIUM", "LOW"
   - IDs must be integers, not strings

2. **Check Ingestion Status**
   - Method: `GET`
   - URL: `http://localhost:8000/status/{ingestion_id}`
   - Replace `{ingestion_id}` with the ID received from the ingest response

### Common Request Errors

1. **Invalid ID Format**

   ```json
   // ❌ Wrong
   {
       "ids": ["id1", "id2", "id3"],
       "priority": "HIGH"
   }

   // ✅ Correct
   {
       "ids": [1, 2, 3],
       "priority": "HIGH"
   }
   ```

2. **Invalid Priority Value**

   ```json
   // ❌ Wrong
   {
       "ids": [1, 2, 3],
       "priority": 2
   }

   // ✅ Correct
   {
       "ids": [1, 2, 3],
       "priority": "HIGH"
   }
   ```

### Example Responses

1. **Successful Ingestion Request**

   ```json
   {
     "ingestion_id": "550e8400-e29b-41d4-a716-446655440000"
   }
   ```

2. **Status Check Response**
   ```json
   {
     "ingestion_id": "550e8400-e29b-41d4-a716-446655440000",
     "status": "triggered",
     "batches": [
       {
         "batch_id": "batch1",
         "ids": [1, 2, 3],
         "status": "completed"
       },
       {
         "batch_id": "batch2",
         "ids": [4, 5],
         "status": "triggered"
       }
     ]
   }
   ```

### Using cURL

```bash
curl -X POST "http://localhost:8000/ingest" \
     -H "Content-Type: application/json" \
     -d '{"ids": [1, 2, 3], "priority": "HIGH"}'
```

## 🔍 Implementation Details

### Priority Processing

- HIGH priority requests are processed first
- MEDIUM priority follows
- LOW priority is processed last
- Within same priority, FIFO order is maintained

### Rate Limiting

- 5-second delay between batch processing
- Applies across all priority levels
- Maintains system stability

### Batch Processing

- Maximum 3 IDs per batch
- Automatic batch splitting
- Individual batch status tracking

## 🚀 Deployment

The API is deployed and live at:

[https://loop-ai-assignment-jzol.onrender.com](https://loop-ai-assignment-jzol.onrender.com)

You can test the endpoints directly using this base URL.

- Health check: [https://loop-ai-assignment-jzol.onrender.com](https://loop-ai-assignment-jzol.onrender.com)
- Example: [https://loop-ai-assignment-jzol.onrender.com/status/<ingestion_id>](https://loop-ai-assignment-jzol.onrender.com/status/%3Cingestion_id%3E)

  ![image](https://github.com/user-attachments/assets/5c39fb5b-644a-4510-94f6-2c824361aea6)


