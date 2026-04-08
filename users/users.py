from fastapi import APIRouter, Depends, HTTPException

import bcrypt

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel, EmailStr

from data.models import User
from data.cre_eng_n_sess import get_db

from users.auth import security

class UserRegisterSchema(BaseModel):
    login: str
    password: str
    email: EmailStr

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register(user: UserRegisterSchema, db: AsyncSession = Depends(get_db)):
    hashed_password =  bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    new_user = User(login=user.login, hash_password=hashed_password, email=user.email)

    db.add(new_user)
    try:
        await db.commit()
        return {"message": "User created successfully!"}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(400, "User already exists")


@router.post("/login")
async def login(user: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    #Get users from BD
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    #//////////

    hashed_password = db_user.hash_password

    if not bcrypt.checkpw(user.password.encode(), hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = security.create_access_token(str(db_user.id))
    return {"access_token": token, "token_type": "bearer"}