import requests
import cv2
import numpy as np
from dtos.generate_spritesheet_dto import GenerateSpriteSheetDTO
from config.config import Settings
from common.util import save_image, remove_bg, crop_vertically

async def generate_image(data:GenerateSpriteSheetDTO):

#   print(data)
  print(Settings().HF_API_KEY)

  API_URL = "https://api-inference.huggingface.co/models/Onodofthenorth/SD_PixelArt_SpriteSheet_Generator"
  headers = {"Authorization": f'Bearer {Settings().HF_API_KEY}'}

  def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

  image_bytes = query({
    "inputs": data.prompt,
  })


  image_array = np.frombuffer(image_bytes, dtype=np.uint8)

  image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
  
  

  return image


async def generate_spritesheet(data:GenerateSpriteSheetDTO):
  ...
  image =  await generate_image(data=data)
  image = remove_bg(image=image)
  image = crop_vertically(image=image)
  save_image(image=image,filename="generation.png")

