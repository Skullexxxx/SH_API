from fastapi import FastAPI

from users.users import router as user_router

from data.cre_eng_n_sess import engine
from data.models import Base

app = FastAPI(title="Avito")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(user_router)