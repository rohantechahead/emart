from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Date, TIMESTAMP, ForeignKey

from common.database import Base


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
    refresh_token = Column(String(255), nullable=True)


class UserAddress(Base):
    __tablename__ = 'useraddresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    address_type = Column(String(50), nullable=False)
    street_address = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(55), nullable=False)
    country = Column(String(55), nullable=False)
    zip_code = Column(String(10), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
