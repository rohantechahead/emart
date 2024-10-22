from typing import Optional, List
import jwt
from fastapi import HTTPException, Header
from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session

from common.constant_helper import SECRET_KEY_TOKENS, ALGORITHM
from services.order_service.app.models import Cart


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

