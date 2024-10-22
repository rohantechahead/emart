from datetime import date
from pydantic import BaseModel


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


class AddressUpdate(BaseModel):
    address_type: str
    street_address: str
    state: str
    country: str
    zip_code: str
    city: str
