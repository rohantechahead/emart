from tokenize import generate_tokens
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from common.constant_helper import STATIC_OTP, DEBUG
from common.database import get_db
from services.user_service.app.models import User
from services.user_service.app.schemas import SignupRequest, LoginRequest
from services.user_service.app.services import create_user, verify_otp, send_otp, generate_otp, generate_access_tokens, \
    generate_refresh_tokens


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
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = create_user(db, request.phone_number, otp_to_send)
    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    send_otp(request.phone_number, otp_to_send)

    return {"message": "OTP sent to your phone number"}


@router.post("/verify-otp")
def verify_otp_route(request: LoginRequest, db: Session = Depends(get_db)):
    # Verify the OTP
    if not verify_otp(db, request.phone_number, request.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Fetch the user from the database based on the phone number
    db_user = db.query(User).filter(User.phone_number == request.phone_number).first()

    # Check if the user exists
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate access and refresh tokens using the user's ID
    access_token = generate_access_tokens(db_user.id)
    refresh_token = generate_refresh_tokens(db_user.id)

    # Return tokens as part of the response
    return {
        "message": "OTP verified, user logged in",
        "access_token": access_token,
        "refresh_token": refresh_token
    }

