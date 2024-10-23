from datetime import datetime, timezone, timedelta
import jwt
from fastapi import HTTPException, Header
from jwt import ExpiredSignatureError

from common.constant_helper import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY_TOKENS, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS


def generate_access_tokens(user_id: int):
    try:
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        payload = {"sub": str(user_id), "exp": expire}
        return jwt.encode(payload, SECRET_KEY_TOKENS, algorithm=ALGORITHM)
    except (ValueError, jwt.PyJWTError) as e:
        print("JWT encoding error:", str(e))
        return None


def generate_refresh_tokens(user_id: int):
    try:
        expire = datetime.now(timezone.utc) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
        payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
        return jwt.encode(payload, SECRET_KEY_TOKENS, algorithm=ALGORITHM)
    except (ValueError, jwt.PyJWTError) as e:
        print("JWT encoding error:", str(e))
        return None


def get_current_user_id_from_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403, detail="Authorization header missing")

    try:

        payload = jwt.decode(authorization, SECRET_KEY_TOKENS, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid token: User ID not found in token")

        return user_id

    except ExpiredSignatureError as e:
        print("JWT decoding error:", str(e))
        raise HTTPException(status_code=403, detail="Session expired please login again")

    except (ValueError, jwt.PyJWTError) as e:
        print("JWT decoding error:", str(e))
        raise HTTPException(status_code=403, detail="Could not validate credentials")
