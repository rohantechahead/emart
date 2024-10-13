import random
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, Header
from common.constant_helper import SECRET_KEY_TOKENS, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS, ACCESS_TOKEN_EXPIRE_MINUTES
from services.user_service.app.models import User


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
        user.is_otp_verified = True
        user.is_login = True
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
    try:
        # Decode the JWT token to get the payload
        payload = jwt.decode(authorization, SECRET_KEY_TOKENS, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")  # Get user ID from the payload

        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid token")

        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")


# def get_current_user_id(authorization: str = Header(None)):
#     if not authorization:
#         raise HTTPException(status_code=403, detail="Authorization header missing")
#
#     try:
#         token = authorization
#         payload = jwt.decode(token, SECRET_KEY_TOKENS, algorithms=[ALGORITHM])
#         user_id: int = payload.get("sub")
#
#         if user_id is None:
#             raise HTTPException(status_code=403, detail="Invalid token: User ID not found in token")
#
#         return user_id
#
#     except (ValueError, jwt.PyJWTError) as e:
#         print("JWT decoding error:", str(e))
#         raise HTTPException(status_code=403, detail="Could not validate credentials")
