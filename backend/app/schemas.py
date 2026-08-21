from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ExceptionResponse(BaseModel):
    id: int
    exception_id: str
    invoice_id: str
    vendor: str

    exception_type: str
    description: str

    expected_value: Optional[float] = None
    actual_value: Optional[float] = None
    difference: Optional[float] = None

    severity: str
    status: str

    confidence: Optional[float] = None
    recommended_action: Optional[str] = None
    ai_reason: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
