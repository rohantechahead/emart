from typing import List
from pydantic import BaseModel

class ProductCategoryCreate(BaseModel):
    name: str

class ProductCategoryUpdate(BaseModel):
    name: str
    status: bool

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int
    status: bool
    image_urls: List[str]

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int
    status: bool


