import random
import uuid

from sqlalchemy.orm import Session

from .models import User, UserAddress


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
        user = User(phone_number=phone_number, uuid=str(uuid.uuid4()))
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
        user.is_login = True
        user.otp = None
        db.commit()
        return True, user
    return False, None


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

    # Commit changes to the database
    db.commit()
    db.refresh(address)

    return address


#
def show_user_detail(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user_info = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "addresses": []
    }
    # Collect the user's addresses
    addresses = db.query(UserAddress).filter(UserAddress.user_id == user_id).all()
    for address in addresses:
        user_info["addresses"].append({
            "address_type": address.address_type,
            "street_address": address.street_address,
            "city": address.city,
            "state": address.state,
            "country": address.country,
            "zip_code": address.zip_code
        })
    return user_info
