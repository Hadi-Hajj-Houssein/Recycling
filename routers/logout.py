from fastapi import APIRouter, Response, Depends, HTTPException
from functionalities.auth import get_curr_user_id, get_curr_company_id

router = APIRouter()

def get_current_user_safe(
    user_id: int = Depends(get_curr_user_id)
) -> int:
    """✅ Try to get user, return user_id if successful"""
    return user_id

def get_current_company_safe(
    company_id: int = Depends(get_curr_company_id)
) -> int:
    """✅ Try to get company, return company_id if successful"""
    return company_id

@router.post("/logout")
def logout(response: Response):
    """
    ✅ Secure logout endpoint for both USER and COMPANY
    - Clears HTTP-only cookie
    - Doesn't require authentication check (user might have expired token)
    - Safe to call anytime
    """
    try:
        # Try to verify user/company (optional - doesn't block logout)
        user_id = Depends(get_curr_user_id)
        company_id = Depends(get_curr_company_id)
    except:
        # Even if token is invalid, we can logout
        pass
    
    # ✅ Clear the authentication cookie
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="lax",
        secure=False,  # Change to True for HTTPS production
    )
    
    return {"message": "Logged out successfully"}