from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()


engine = create_async_engine(
    os.environ.get('DATABASE_URL'),
    echo=True,
)


AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
     async with AsyncSessionLocal() as session:
         yield session

