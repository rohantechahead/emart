from pydantic import BaseModel


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int


# Response model for displaying cart items
class CartItem(BaseModel):
    id: int
    product_id: int
