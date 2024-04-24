from fastapi import FastAPI


from auth.jwt_bearer import JWTBearer
from config.config import initiate_database,iinitiate_firebase
from routes.generate import GenerateRouter


app = FastAPI()


token_listener = JWTBearer()



@app.on_event("startup")
async def start_database():
    await initiate_database()
    await iinitiate_firebase()


@app.post("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}


app.include_router(GenerateRouter,tags=["Generation"],prefix="/generate",)
