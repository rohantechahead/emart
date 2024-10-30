from datetime import date
from pydantic import BaseModel

class SignupRequest(BaseModel):
    phone_number: str
    country_code: str


class LoginRequest(BaseModel):
    phone_number: str
    otp: str
    country_code: str


class UpdateProfileRequest(BaseModel):
    first_name: str
    last_name: str
    dob: date
    gender: str

class Address(BaseModel):
    address_type: str
    street_address: str
    city: str
    state: str
    country: str
    zip_code: str

