from typing import Optional, List
import httpx
import jwt
from fastapi import HTTPException, Header
from jwt import ExpiredSignatureError
from sqlalchemy import func
from sqlalchemy.orm import Session
from common.constant_helper import SECRET_KEY_TOKENS, ALGORITHM
from services.order_service.app.models import Cart, OrderItem, Order
from services.order_service.app.schemas.response_schemas import OrderItemResponse, OrderResponse


def add_or_update_cart_item(db: Session, user_id: int, product_id: int, quantity: int):
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()

    if cart_item:
        cart_item.quantity += quantity
        cart_item.updated_at = func.now()
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item


def get_current_user_id(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403, detail="Authorization header missing")

    try:
        payload = jwt.decode(authorization, SECRET_KEY_TOKENS, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid token: User ID not found in token")

        return user_id

    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Session expired, please login again")

    except (ValueError, jwt.PyJWTError) as e:
        print("JWT decoding error:", str(e))
        raise HTTPException(status_code=403, detail="Could not validate credentials")

def get_user_cart_items(db: Session, user_id: int) -> List[Cart]:
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    return cart_items


def remove_cart_item(db: Session, user_id: int, product_id: int):
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db.delete(cart_item)
    db.commit()
    return {"detail": "Item removed from cart"}


async def place_order_from_cart(db: Session, user_id: int):
    # Query cart items
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Your cart is empty")

    product_ids = [cart_item.product_id for cart_item in cart_items]
    product_details_map = await get_product_details_batch(product_ids)

    total_amount = 0
    order_items = []

    for cart_item in cart_items:
        product_detail = product_details_map.get(cart_item.product_id)
        if product_detail:
            total_amount += product_detail["price"] * cart_item.quantity
            order_items.append(OrderItem(
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=product_detail["price"]
            ))

    # Create the order
    new_order = Order(user_id=user_id, total_amount=total_amount)
    db.add(new_order)
    db.commit()

    for item in order_items:
        item.order_id = new_order.id

    db.bulk_save_objects(order_items)

    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()

    return OrderResponse(
        id=new_order.id,
        total_amount=total_amount,
        order_items=[
            OrderItemResponse(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price
            ) for item in order_items
        ]
    )



async def get_product_details_batch(product_ids: List[int]):
    if not product_ids:
        return {}

    product_service_url = f"http://localhost:8000/products?product_ids={','.join(map(str, product_ids))}"

    async with httpx.AsyncClient() as client:
        response = await client.get(product_service_url)

    if response.status_code == 200:
        return {item["id"]: item for item in response.json()}
    return {}





