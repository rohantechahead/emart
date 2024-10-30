from typing import List

from pydantic import BaseModel

# Response model for displaying cart items
class CartItem(BaseModel):
    id: int
    product_id: int
#
class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    order_items: List[OrderItemResponse]
