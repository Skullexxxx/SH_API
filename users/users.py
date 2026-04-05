from fastapi import APIRouter
from sqlalchemy.testing.pickleable import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register():
    return {"message": "user registered"}