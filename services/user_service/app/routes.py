from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from common.database import get_db
from .models import User
from .schemas import SignupRequest, LoginRequest
from .services import create_user, verify_otp

router = APIRouter()


@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = create_user(db, request.phone_number)
    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    return {"message": "OTP sent to your phone number"}


@router.post("/verify-otp")
def verify_otp_route(request: LoginRequest, db: Session = Depends(get_db)):
    if not verify_otp(db, request.phone_number, request.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return {"message": "OTP verified, user logged in"}
