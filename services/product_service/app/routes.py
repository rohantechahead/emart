from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from common.database import get_db
from services.product_service.app.schemas import ProductCategoryResponse, ProductCategoryCreate, ProductCategoryUpdate, \
    ProductCreate, ProductUpdateResponse, ProductUpdate, ProductResponse
from services.product_service.app.services import create_category, update_category, delete_category, \
    search_category_by_name, create_product, update_product_by_id, delete_product, get_products

router = APIRouter()


@router.get("/")
def index():
    return {"message": "hello welcome to Product Services"}


@router.post("/categories/", response_model=ProductCategoryResponse)
def create_product_category(category: ProductCategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category)


@router.put("/Update-categories/{category_id}", response_model=ProductCategoryResponse)
def update_product_category(category_id: int, category_update: ProductCategoryUpdate, db: Session = Depends(get_db)):
    category = update_category(db, category_id, category_update)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/Delete-categories/{category_id}")
def delete_product_category(category_id: int, db: Session = Depends(get_db)):
    category = delete_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}


@router.get("/Search-categories/", response_model=list[ProductCategoryResponse])
def search_or_list_categories(search: str = None, db: Session = Depends(get_db)):
    return search_category_by_name(db, search_query=search)


@router.post("/Create-new-products/")
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    create_product(db, product)
    return {"message": "Product operation successful"}


@router.put("/products/update/{product_id}", response_model=ProductUpdateResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product_by_id(db, product_id, product_update)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found for the given product ID")
    return product


@router.delete("/Delete-products/{product_id}")
def delete_product_item(product_id: int, db: Session = Depends(get_db)):
    product = delete_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}


@router.get("/products", response_model=Union[ProductResponse, List[ProductResponse]])
def search_products(product_id: int = None, db: Session = Depends(get_db)):
    product = get_products(db, product_id)
    if product_id is not None and product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product if product_id is not None else product
