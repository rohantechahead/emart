from pydantic import BaseModel


class SignupRequest(BaseModel):
    phone_number: str


class LoginRequest(BaseModel):
    phone_number: str
    otp: str
