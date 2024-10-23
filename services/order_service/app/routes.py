from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from common.database import get_db
from services.order_service.app.schemas.request_schemas import CartItemCreate
from services.order_service.app.schemas.response_schemas import CartItem

from services.order_service.app.services import get_current_user_id, get_user_cart_items, remove_cart_item, \
    add_or_update_cart_item

router = APIRouter()


@router.post("/add-to-cart", response_model=CartItem)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    cart_item = add_or_update_cart_item(db, user_id, item.product_id, item.quantity)
    return cart_item

@router.get("/view-cart", response_model=List[CartItem])
def view_cart_items(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return get_user_cart_items(db, user_id)

@router.delete("/remove-from-cart/{product_id}", response_model=dict)
def remove_cart_item_route(product_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return remove_cart_item(db, user_id, product_id)

