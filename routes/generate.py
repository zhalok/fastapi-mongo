from fastapi import Body, APIRouter, HTTPException
from dtos.create_spritesheet_dto import CreateSpriteSheetDTO

GenerateRouter = APIRouter()

@GenerateRouter.post("/spritesheet")
async def generate_spritesheet(create_spritesheet_dto:CreateSpriteSheetDTO = Body(...)):
    ...
    return create_spritesheet_dto.prompt