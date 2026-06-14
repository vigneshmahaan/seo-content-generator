from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class SEORequest(BaseModel):
    id: Optional[int] = None
    input_one: str = Field(..., alias="input_one")
    input_two: str = Field(..., alias="input_two")
    input_three: Optional[str] = Field(None, alias="input_three")
    status: str = Field("Pending")
    provider_used: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("input_one", "input_two")
    def not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Input fields input_one and input_two are required")
        return value.strip()
