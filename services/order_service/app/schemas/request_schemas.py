from typing import List
from pydantic import BaseModel


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

#
class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int

class OrderRequest(BaseModel):
    order_items: List[OrderItemRequest]

