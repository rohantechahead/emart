from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(15), unique=True, nullable=False, index=True)
    otp = Column(String(6), nullable=True)  # Storing the OTP temporarily
    is_otp_verified = Column(Boolean, default=False)  # OTP verified or not
    is_login = Column(Boolean, default=False)  # Tracking if the user is logged in
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    profile_image = Column(String(512), nullable=True)
    status = Column(Boolean, default=True)
    dob = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    reference_token =Column(String(15),nullable=True)

