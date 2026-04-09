from fastapi import (APIRouter, Depends,
                     HTTPException, Response,)

import bcrypt

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel, EmailStr

from data.models import User
from data.cre_eng_n_sess import get_db

from users.auth import security, config

class UserRegisterSchema(BaseModel):
    login: str
    password: str
    email: EmailStr

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

router = APIRouter(prefix="/users", tags=["users"])



"""
    1.Get login, password and email
    2.Hash password
    3.Create new user in database
"""
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





"""
    1.Get email and password
    2.Search user in database
    3.Check hashed password
    4.Give cookie token
"""
@router.post("/login")
async def login(user: UserLoginSchema,
                response: Response,
                db: AsyncSession = Depends(get_db)):

    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    hashed_password = db_user.hash_password

    if not bcrypt.checkpw(user.password.encode(), hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = security.create_access_token(str(db_user.id))
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/protected", dependencies=[Depends(security.access_token_required)] )
async def protected():

    return {"message": "Hello World"}