from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class IngestRequest(BaseModel):
    ids: List[int] = Field(..., description="List of IDs to process")
    priority: Priority = Field(..., description="Priority level for processing")
