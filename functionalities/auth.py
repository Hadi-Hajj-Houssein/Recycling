from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, Cookie

NGU = "~`3781678^&*^^roro!&%#^%&^!*)(&%$^*N!)(*M7nhadi42868&!)&#^$)(*!(&Btrgnhm(^!(THK*^(@$&^% ?/>,.,<<<>,6M7*&m@ t!*&oIUGHXharde#tp@$sNJS))))"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes: int = 15):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload["exp"] = expire
    return jwt.encode(payload, NGU, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, NGU, algorithms=[ALGORITHM])

def get_curr_user_id(access_token: str | None = Cookie(default=None, alias="access_token")):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_token(access_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return int(user_id)