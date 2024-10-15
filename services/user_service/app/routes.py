from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from common.constant_helper import STATIC_OTP, DEBUG
from common.database import get_db
from services.user_service.app.models import User
from services.user_service.app.schemas import SignupRequest, LoginRequest, UpdateProfileRequest, AddressUpdate
from services.user_service.app.services import create_user, verify_otp, send_otp, generate_otp, generate_access_tokens, \
    generate_refresh_tokens, get_current_user_id_from_token, create_address, update_address

router = APIRouter()

otp_to_send = STATIC_OTP if DEBUG else generate_otp()


@router.get("/")
def index():
    return {"message": "hello welcome to User Services"}


@router.get("/health")
def health_check():
    return {"message": "All well!!!"}


@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    new_user = False
    if not user:
        new_user = create_user(db, request.phone_number, otp_to_send)
    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    send_otp(request.phone_number, otp_to_send)

    return {"message": "OTP sent to your phone number"}


@router.post("/verify-otp")
def verify_otp_route(request: LoginRequest, db: Session = Depends(get_db)):
    # Verify the OTP
    is_verified, user = verify_otp(db, request.phone_number, request.otp)

    if not is_verified:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    

    # Check if the user exists
    if not user:
        raise HTTPException(status_code=404, detail="invalid user")

    # Generate access and refresh tokens using the user's ID
    access_token = generate_access_tokens(user.id)
    refresh_token = generate_refresh_tokens(user.id)
    user.refresh_token = refresh_token
    db.commit()

    # Return tokens as part of the response
    return {
        "message": "OTP verified, user logged in",
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.put("/profile-update")
def update_profile(request: UpdateProfileRequest, db: Session = Depends(get_db),
                   user_id: int = Depends(get_current_user_id_from_token)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's profile with the provided fields
    if request.first_name:
        user.first_name = request.first_name
    if request.last_name:
        user.last_name = request.last_name
    if request.gender:
        user.gender = request.gender
    if request.dob:
        user.dob = request.dob

    db.commit()  # Save changes to the database
    db.refresh(user)  # Refresh the instance to get the latest data

    return {"message": "Profile updated successfully", "user": user}


@router.put("/logout")
def logout(user_id: int = Depends(get_current_user_id_from_token), db: Session = Depends(get_db)):
    """Log out the user by clearing the reference token."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Set the reference token to None
    user.refresh_token = None
    user.is_login = False
    db.commit()

    return {"message": "User logged out successfully"}


@router.post("/create-address")
def create_new_address(request: AddressUpdate, db: Session = Depends(get_db),
                       user_id: int = Depends(get_current_user_id_from_token)):
    new_address = create_address(
        db, user_id=user_id, address_type=request.address_type,
        street_address=request.street_address, city=request.city,
        state=request.state, country=request.country, zip_code=request.zip_code
    )

    return {"message": "Address created successfully", "address": new_address}


@router.put("/update-address/{address_id}")
def update_existing_address(address_id: int, request: AddressUpdate,
                            db: Session = Depends(get_db),
                            user_id: int = Depends(get_current_user_id_from_token)):
    updated_address = update_address(
        db, user_id=user_id, address_id=address_id,
        address_type=request.address_type, street_address=request.street_address,
        city=request.city, state=request.state, country=request.country,
        zip_code=request.zip_code
    )

    if updated_address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    return {"message": "Address updated successfully", "address": updated_address}
