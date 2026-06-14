from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SEOContent(BaseModel):
    id: Optional[int] = None
    request_id: int = Field(..., alias="request_id")
    generated_content: str = Field(..., alias="generated_content")
    generated_at: Optional[datetime] = None
