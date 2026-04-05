from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from data.models import UserSchema
from data.cre_eng_n_sess import get_db


class User(BaseModel):
    login: str
    password: str
    email: EmailStr

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register(user: User, db: AsyncSession = Depends(get_db)):
    new_user = UserSchema(login=user.login, password=user.password, email=user.email)

    db.add(new_user)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("User already exists")
