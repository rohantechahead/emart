from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from common.authentication_helper import get_current_user_id_from_token, generate_access_tokens, generate_refresh_tokens
from common.common_message import Message
from common.constant_helper import STATIC_OTP, DEBUG
from common.database import get_db
from .models import User
from .schemas.request_schemas import SignupRequest, LoginRequest, UpdateProfileRequest, Address
from .schemas.response_schemas import UserProfileResponse, AddressUpdate, OTPVerificationResponse, ProfileUpdateResponse
from .services import create_user, send_otp, generate_otp, update_address, show_user_detail, verify_otp, create_address

router = APIRouter()
common_message = Message()

otp_to_send = STATIC_OTP if DEBUG else generate_otp()


@router.get("/")
def index():
    return {common_message.user_greet}


@router.get("/health")
def health_check():
    return {common_message.all_well}


@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    if not user:
        user = create_user(db, request.phone_number, otp_to_send, request.country_code)
    if not user:
        raise HTTPException(status_code=500, detail=common_message.fail_message)
    user.otp = otp_to_send
    db.commit()
    send_otp(f"{request.country_code}{request.phone_number}", otp_to_send)

    return {common_message.otp_message}


@router.post("/verify-otp", response_model=OTPVerificationResponse)
def verify_otp_route(request: LoginRequest, db: Session = Depends(get_db)):

    is_verified, user = verify_otp(db, request.phone_number, request.otp, request.country_code)

    if not is_verified:
        raise HTTPException(status_code=400, detail=common_message.invalid_otp)
    if not user:
        raise HTTPException(status_code=404, detail=common_message.user_detail)

    access_token = generate_access_tokens(user.id)
    refresh_token = generate_refresh_tokens(user.id)
    user.refresh_token = refresh_token
    db.commit()

    return {"user_id": user.id, "access_token": access_token, "refresh_token": refresh_token}


@router.put("/profile-update", response_model=ProfileUpdateResponse)
def update_profile(request: UpdateProfileRequest, db: Session = Depends(get_db),
                   user_id: int = Depends(get_current_user_id_from_token)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=common_message.user_detail)

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

    return user


@router.put("/logout")
def logout(user_id: int = Depends(get_current_user_id_from_token), db: Session = Depends(get_db)):
    """Log out the user by clearing the reference token."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=common_message.user_detail)

    # Set the reference token to None
    user.refresh_token = None
    user.is_login = False
    db.commit()

    return {common_message.logout_message}


@router.post("/create-address")
def create_new_address(request: AddressUpdate, db: Session = Depends(get_db),
                       user_id: int = Depends(get_current_user_id_from_token)):
    # Call the create_address function
    create_address(
        db, user_id=user_id, address_type=request.address_type,
        street_address=request.street_address, city=request.city,
        state=request.state, country=request.country, zip_code=request.zip_code
    )


    return {common_message.create_message}


@router.put("/update-address/{address_id}", response_model=Address)
def update_existing_address(address_id: int, request: Address,
                            db: Session = Depends(get_db),
                            user_id: int = Depends(get_current_user_id_from_token)):
    print("address_id", address_id)
    updated_address = update_address(db, user_id=user_id, address_id=address_id, **request.dict())
    if updated_address is None:
        raise HTTPException(status_code=404, detail=common_message.add_missing)
    return updated_address


@router.get("/user-detail", response_model=UserProfileResponse)
def user_detail(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id_from_token)):
    user_info = show_user_detail(db, user_id)
    if not user_info:
        raise HTTPException(status_code=404, detail=common_message.user_detail)
    return user_info
