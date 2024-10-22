from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from common.database import get_db
from services.order_service.app import models
from services.order_service.app.models import Cart
from services.order_service.app.schemas import CartItemCreate, CartItem
from services.order_service.app.services import get_current_user_id, get_user_cart_items, remove_cart_item

router = APIRouter()


@router.post("/add-to-cart", response_model=CartItem)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    cart_item = db.query(Cart).filter(Cart.user_id == user_id,
                                      Cart.product_id == item.product_id).first()
    if cart_item:
        cart_item.quantity += item.quantity
        cart_item.updated_at = func.now()
    else:
        cart_item = models.Cart(user_id=user_id, product_id=item.product_id, quantity=item.quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.get("/view-cart", response_model=List[CartItem])
def view_cart_items(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return get_user_cart_items(db, user_id)

@router.delete("/remove-from-cart/{product_id}", response_model=dict)
def remove_cart_item_route(product_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return remove_cart_item(db, user_id, product_id)

