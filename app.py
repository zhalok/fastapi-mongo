from fastapi import FastAPI, Depends

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.generate import GenerateRouter

app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}


# app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
# app.include_router(StudentRouter,tags=["Students"],prefix="/student",dependencies=[Depends(token_listener)],)
app.include_router(GenerateRouter,tags=["Generation"],prefix="/generate",)