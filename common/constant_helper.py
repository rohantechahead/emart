import os

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
STATIC_OTP = os.getenv("STATIC_OTP")

DEBUG = True if os.getenv("DEBUG") == "True" else False
