import random

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


def create_user(db, phone_number: str):
    """Create a new user with phone number"""
    try:
        otp = generate_otp()
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
