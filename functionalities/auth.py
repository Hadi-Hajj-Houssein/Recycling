# functionalities/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt # You might need to pip install python-jose[cryptography]

# CONFIGURATION (In a real app, put these in an .env file)
SECRET_KEY = "YOUR_SECRET_KEY_HERE" # Must match the one you used to sign the token in login.py
ALGORITHM = "HS256"

# This automatically looks for the "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decode the token (Verify signature)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 2. Get the User ID (assuming you saved it as "sub" or "user_id" when logging in)
        user_id: str = payload.get("sub") 
        
        if user_id is None:
            raise credentials_exception
            
        # 3. Return the ID (or fetch the full user from DB if you prefer)
        return user_id
        
    except JWTError:
        raise credentials_exception