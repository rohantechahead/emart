from pydantic import BaseModel

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int

class ProductUpdateResponse(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int
    status: bool

class ProductCategoryResponse(BaseModel):
    id: int
    name: str
    status: bool