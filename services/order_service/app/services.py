from typing import Optional
import jwt
from fastapi import HTTPException, Header
from jwt import ExpiredSignatureError

from common.constant_helper import SECRET_KEY_TOKENS, ALGORITHM


def get_current_user_id(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403, detail="Authorization header missing")

    try:
        # Decode the JWT token from the Authorization header
        payload = jwt.decode(authorization, SECRET_KEY_TOKENS, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")  # Typically, "sub" is used for user IDs

        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid token: User ID not found in token")

        return user_id  # Return the user ID if valid

    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Session expired, please login again")

    except (ValueError, jwt.PyJWTError) as e:
        print("JWT decoding error:", str(e))
        raise HTTPException(status_code=403, detail="Could not validate credentials")
