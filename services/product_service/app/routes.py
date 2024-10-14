from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from common.database import get_db
from services.product_service.app.schemas import ProductCategoryResponse, ProductCategoryCreate, ProductCategoryUpdate
from services.product_service.app.services import create_category, update_category, delete_category, \
    search_category_by_name

router = APIRouter()

@router.get("/")
def index():
    return {"message": "hello welcome to Product Services"}

@router.post("/categories/", response_model=ProductCategoryResponse)
def create_product_category(category: ProductCategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category)

# Update a category by ID (name and status)
@router.put("/Update-categories/{category_id}", response_model=ProductCategoryResponse)
def update_product_category(category_id: int, category_update: ProductCategoryUpdate, db: Session = Depends(get_db)):
    category = update_category(db, category_id, category_update)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Delete a category by ID
@router.delete("/Delete-categories/{category_id}")
def delete_product_category(category_id: int, db: Session = Depends(get_db)):
    category = delete_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}

# Search category by title or get all if no search query
@router.get("/Search-categories/", response_model=list[ProductCategoryResponse])
def search_or_list_categories(search: str = None, db: Session = Depends(get_db)):
    return search_category_by_name(db, search_query=search)

