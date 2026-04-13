from fastapi import APIRouter, Response

router = APIRouter()

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="lax",
        secure=False  # must match exactly what you set in login
    )
    return {"message": "Logged out"}