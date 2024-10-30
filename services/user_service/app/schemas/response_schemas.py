from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class AddressUpdate(BaseModel):
    id: int
    address_type: str
    street_address: str
    city: str
    state: str
    country: str
    zip_code: str


class UserProfileResponse(BaseModel):
    id: int
    phone_number: str
    country_code: str
    first_name: str
    last_name: str
    dob: date
    gender: str
    is_otp_verified: bool
    is_login: bool
    profile_image: Optional[str]
    addresses: List[AddressUpdate]

    class Config:
        from_attributes = True


class OTPVerificationResponse(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str


class ProfileUpdateResponse(BaseModel):
    id: int
    phone_number: str
    first_name: str
    last_name: str
    dob: date
    gender: str
