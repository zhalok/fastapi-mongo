from fastapi import Body, APIRouter, HTTPException
from dtos.generate_spritesheet_dto import GenerateSpriteSheetDTO
from services import generate
GenerateRouter = APIRouter()

@GenerateRouter.post("/spritesheet")
async def generate_spritesheet(generate_spritesheet_dto:GenerateSpriteSheetDTO = Body(...)):
    ...
    response =  await generate.generate_spritesheet(generate_spritesheet_dto)
    json_response = { "success": True, "data":response, "message": None }
    return json_response