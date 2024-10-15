from pydantic import BaseModel


class ProductCategoryCreate(BaseModel):
    name: str

class ProductCategoryUpdate(BaseModel):
    name: str
    status: bool

class ProductCategoryResponse(BaseModel):
    id: int
    name: str
    status: bool


