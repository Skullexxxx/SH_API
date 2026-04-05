from fastapi import FastAPI

from users.users import router as user_router

app = FastAPI(title="Avito")


app.include_router(user_router)