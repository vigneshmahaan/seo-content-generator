from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SystemLog(BaseModel):
    id: Optional[int] = None
    request_id: Optional[int] = Field(None, alias="request_id")
    log_type: str = Field(..., alias="log_type")
    message: str
    provider: Optional[str] = None
    created_at: Optional[datetime] = None
