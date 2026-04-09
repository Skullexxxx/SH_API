from fastapi import FastAPI


from users.users import router as user_router

from data.cre_eng_n_sess import engine
from data.models import Base

from authx.exceptions import MissingTokenError

from hand_err import error_response

app = FastAPI(title="Avito")



@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.exception_handler(MissingTokenError)
async def missing_token_handler(request, exc):
    return error_response(
        code="AUTH_001",
        message="Not authenticated",
        status_code=401
    )


app.include_router(user_router)