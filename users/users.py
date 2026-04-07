from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel, EmailStr

from data.models import User
from data.cre_eng_n_sess import get_db


class UserRegisterShcems(BaseModel):
    login: str
    password: str
    email: EmailStr

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register(user: UserRegisterShcems, db: AsyncSession = Depends(get_db)):
    new_user = User(login=user.login, password=user.password, email=user.email)

    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(400, "User already exists")


@router.post("/login")
async def login(user: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)

    return result.scalars().first()

