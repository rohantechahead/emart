import random
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, Header
from jwt import ExpiredSignatureError
from sqlalchemy import func
from sqlalchemy.orm import Session

from common.constant_helper import SECRET_KEY_TOKENS, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS, ACCESS_TOKEN_EXPIRE_MINUTES
from services.user_service.app.models import User, UserAddress



def generate_otp():
    """Generates a 6-digit OTP."""
    return str(random.randint(100000, 999999))


def send_otp(phone_number, otp):
    """
    Simulates sending the OTP to the user's phone.
    Replace this with an SMS gateway like Twilio or AWS SNS.
    """
    print(f"Sending OTP {otp} to {phone_number}")
    # Replace this with actual SMS sending logic


def create_user(db, phone_number: str, otp: str):
    """Create a new user with phone number"""
    try:
        send_otp(phone_number, otp)
        user = User(phone_number=phone_number, otp=otp)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        print(e)
        db.rollback()
        return None


def verify_otp(db, phone_number: str, otp: str):
    """Verify the OTP entered by the user"""
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if user and user.otp == otp:
        user.is_verified = True
        user.is_login = True
        user.is_login = True
        user.otp = None
        db.commit()
        return True, user
    return False, None


def generate_access_tokens(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY_TOKENS, algorithm=ALGORITHM)


def generate_refresh_tokens(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
    payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
    return jwt.encode(payload, SECRET_KEY_TOKENS, algorithm=ALGORITHM)




def get_current_user_id_from_token(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(status_code=403, detail="Authorization header missing")


    try:

        payload = jwt.decode(authorization, SECRET_KEY_TOKENS, algorithms=[ALGORITHM])

        user_id: int = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid token: User ID not found in token")

        return user_id

    except ExpiredSignatureError as e:
        print("JWT decoding error:", str(e))
        raise HTTPException(status_code=403, detail="Session expired please login again")



    except (ValueError, jwt.PyJWTError) as e:
        print("JWT decoding error:", str(e))
        raise HTTPException(status_code=403, detail="Could not validate credentials")


def create_address(db: Session, user_id: int, address_type: str, street_address: str, city: str,
                   state: str, country: str, zip_code: str):
    # Create a new address for the user
    new_address = UserAddress(user_id=user_id, address_type=address_type,
                              street_address=street_address, city=city,
                              state=state, country=country, zip_code=zip_code)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)  # Refresh to get the newly inserted data

    return new_address
def update_address(db: Session, user_id: int, address_id: int, address_type: str = None,
                   street_address: str = None, city: str = None, state: str = None,
                   country: str = None, zip_code: str = None):
    # Fetch the address by ID and ensure it belongs to the user
    address = db.query(UserAddress).filter(UserAddress.user_id == user_id,
                                           UserAddress.id == address_id).first()

    if not address:
        return None  # Address not found

    # Update address fields if they are provided
    if address_type:
        address.address_type = address_type
    if street_address:
        address.street_address = street_address
    if city:
        address.city = city
    if state:
        address.state = state
    if country:
        address.country = country
    if zip_code:
        address.zip_code = zip_code

    # Update the timestamp
    address.updated_at = func.now()

    # Commit changes to the database
    db.commit()
    db.refresh(address)

    return address

