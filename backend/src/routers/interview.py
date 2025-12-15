from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/api/ai/question")
async def create_question():
    