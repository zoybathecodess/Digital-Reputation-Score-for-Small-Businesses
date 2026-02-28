from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CreateOrderRequest(BaseModel):
    tenant_id: str
    contact_id: str
    whatsapp_account_id: str
    inquiry_id: str
    items: List[dict] = Field(..., description="List of order items")
    total_amount: float
    currency: str = "XAF"
    payment_method: str = "momo"
    notes: Optional[str] = None

class OrderItem(BaseModel):
    product_name: str
    quantity: int
    unit_price: float
    total_price: float

class OrderResponse(BaseModel):
    id: str
    tenant_id: str
    contact_id: str
    whatsapp_account_id: str
    inquiry_id: str
    order_number: str
    items: List[OrderItem]
    total_amount: float
    currency: str
    payment_method: str
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

class OrderUpdateRequest(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    payment_status: Optional[str] = None
