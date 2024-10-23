from pydantic import BaseModel

# Response model for displaying cart items
class CartItem(BaseModel):
    id: int
    product_id: int