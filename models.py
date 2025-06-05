from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import List

class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class IngestRequest(BaseModel):
    ids: List[int] = Field(
        ...,
        description="List of IDs to process (range: 1 to 10^9+7)",
        min_items=1
    )
    priority: Priority = Field(
        ...,
        description="Priority level for processing (HIGH, MEDIUM, LOW)"
    )

    @validator('ids')
    def validate_ids(cls, v):
        if not v:
            raise ValueError("IDs list cannot be empty")
        
        for id in v:
            if not isinstance(id, int):
                raise ValueError(f"ID must be an integer, got {type(id)}")
            if id < 1 or id > 10**9 + 7:
                raise ValueError(f"ID must be between 1 and 10^9+7, got {id}")
        return v

    @validator('priority')
    def validate_priority(cls, v):
        if not isinstance(v, Priority):
            raise ValueError(f"Priority must be one of {[p.value for p in Priority]}")
        return v
