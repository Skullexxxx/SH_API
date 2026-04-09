from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from users.users import router as user_router

from data.cre_eng_n_sess import engine
from data.models import Base

from authx.exceptions import MissingTokenError

app = FastAPI(title="Avito")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.exception_handler(MissingTokenError)
async def missing_token(request: Request, exc: MissingTokenError):
    return JSONResponse(status_code=401,
                        content={"message": "Token is missing!"})
app.include_router(user_router)