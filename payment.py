from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PaymentCreateRequest(BaseModel):
    order_id: str
    amount: float
    currency: str = "XAF"
    payment_method: str = "momo"
    phone_number: Optional[str] = None
    notes: Optional[str] = None

class PaymentResponse(BaseModel):
    id: str
    order_id: str
    amount: float
    currency: str
    payment_method: str
    status: str
    transaction_id: Optional[str]
    phone_number: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
