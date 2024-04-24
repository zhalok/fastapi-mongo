from fastapi import Body, APIRouter, HTTPException
from dtos.generate_spritesheet_dto import GenerateSpriteSheetDTO
from services import generate
GenerateRouter = APIRouter()

@GenerateRouter.post("/spritesheet")
async def generate_spritesheet(generate_spritesheet_dto:GenerateSpriteSheetDTO = Body(...)):
    ...
    await generate.generate_spritesheet(generate_spritesheet_dto)
    return "cool"