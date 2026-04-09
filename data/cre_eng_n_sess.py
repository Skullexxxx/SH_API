from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

"""Create async engine"""
engine = create_async_engine(
    os.environ.get('DATABASE_URL'),
    echo=True,
)

"""Create async session"""
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
"""func for working with database"""
async def get_db():
     async with AsyncSessionLocal() as session:
         yield session

