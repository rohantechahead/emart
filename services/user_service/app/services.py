import random
from datetime import datetime, timedelta
import jwt
from services.user_service.app.models import User

SECRET_KEY = "22ea3d2d7418871717c3bf855db449849a9cd85a1350a9ef67f3e5f5aaa85f23"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

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
        return True
    return False

def generate_access_tokens(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def generate_refresh_tokens(user_id: int):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)