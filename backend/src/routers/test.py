from fastapi import APIRouter, Depends
from src.core.auth import get_current_user

router = APIRouter(prefix="/api/test", tags=["test"])


@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    return {"message": "인증 성공!", "user": user}
