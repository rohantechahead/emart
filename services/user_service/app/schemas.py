from datetime import date
from pydantic import BaseModel


class SignupRequest(BaseModel):
    phone_number: str


class LoginRequest(BaseModel):
    phone_number: str
    otp: str


class UserProfileResponse(BaseModel):
    id: int
    phone_number: str
    first_name: str
    last_name: str
    dob: date
    gender: str
    is_otp_verified: bool
    is_login: bool
    profile_image: str | None

    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    first_name: str
    last_name: str
    dob: date
    gender: str


class AddressUpdate(BaseModel):
    address_type: str
    street_address: str
    state: str
    country: str
    zip_code: str
    city: str
