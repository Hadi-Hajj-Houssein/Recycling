from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
NGU = "~`3781678^&*^^roro!&%#^%&^!*)(&%$^*N!)(*M7nhadi42868&!)&#^$)(*!(&Btrgnhm(^!(THK*^(@$&^% ?/>,.,<<<>,6M7*&m@ t!*&oIUGHXharde#tp@$sNJS))))"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
def  create_access_token(data: dict, expires_minutes: int = 15):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload["exp"] = expire
    return jwt.encode(payload, NGU, algorithm=ALGORITHM)

def get_curr_user_id(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, NGU, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def decode_token(token:str):
    return jwt.decode(token,NGU,algorithms=[ALGORITHM] )
