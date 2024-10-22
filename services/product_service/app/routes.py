from typing import List, Union, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from common.common_message import Message
from common.database import get_db
from .models import Product
from .schemas import ProductCategoryResponse, ProductCategoryCreate, ProductCategoryUpdate, ProductCreate, \
    ProductUpdateResponse, ProductUpdate, ProductResponse
from .services import create_category, update_category, delete_category, search_category_by_name, create_product, \
    update_product_by_id, delete_product, get_products

common_message = Message()

router = APIRouter()

@router.get("/")
def index():
    return {common_message.product_greet}

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
    return {common_message.category_delete}


@router.get("/Search-categories/", response_model=list[ProductCategoryResponse])
def search_or_list_categories(search: str = None, db: Session = Depends(get_db)):
    return search_category_by_name(db, search_query=search)


@router.post("/Create-new-products/")
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    create_product(db, product)
    return {common_message.product_create}

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

    return {common_message.delete_message}

@router.get("/products", response_model=Union[ProductResponse, List[ProductResponse]])
def search_products(product_id: int = None, db: Session = Depends(get_db)):
    product = get_products(db, product_id)
    if product_id is not None and product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@router.get("/user/product-search/", response_model=Union[ProductResponse, List[ProductResponse]])
def product_search_by_filter(
        category_id: int,
        search_key: Optional[str] = Query(None,
                                          description="Search keyword (optional, used only if category_id is provided)"),
        min_price: Optional[float] = Query(None,
                                           description="Minimum price (optional, used only if category_id is provided)"),
        max_price: Optional[float] = Query(None,
                                           description="Maximum price (optional, used only if category_id is provided)"),
        db: Session = Depends(get_db),
):
    # Ensure category_id is valid
    if category_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid category ID")

    # Query products based on the provided category_id
    query = db.query(Product).filter(Product.category_id == category_id)

    # Apply search_key filter
    if search_key:
        search_key = f"%{search_key}%"
        query = query.filter(Product.name.ilike(search_key))

    # Apply price range filter
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.all()
    return products
