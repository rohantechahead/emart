from datetime import date
from typing import Optional

from pydantic import BaseModel


class SignupRequest(BaseModel):
    phone_number: str


class LoginRequest(BaseModel):
    phone_number: str
    otp: str


class Response(BaseModel):
    id: int
    phone_number: str
    otp: str
    access_token: str
    refresh_token: str


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
