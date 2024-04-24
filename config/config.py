from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
import models as models
import firebase_admin




class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None
    HF_API_KEY:str 
    # FIREBASE_PRIVATE_KEY_ID:str
    FIREBASE_PRIVATE_KEY:str
    FIREBASE_PROJECT_ID:str
    FIREBASE_CLIENT_EMAIL:str

    # JWT
    secret_key: str = "secret"
    algorithm: str = "HS256"

    class Config:
        env_file = ".env.dev"
        from_attributes = True




async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(), document_models=models.__all__
    )


async def iinitiate_firebase():
    env = Settings()
    config = {
    "type":"service_account",
    "client_email": env.FIREBASE_CLIENT_EMAIL,
    "project_id": env.FIREBASE_PROJECT_ID,
    "token_uri": "https://oauth2.googleapis.com/token",
    "private_key": env.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
   
    }


    cred = firebase_admin.credentials.Certificate(config)
    firebase_admin.initialize_app(cred,{ "storageBucket":"learnyx-962bf.appspot.com"})
    
