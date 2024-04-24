import requests
import cv2
import numpy as np
from dtos.generate_spritesheet_dto import GenerateSpriteSheetDTO
from config.config import Settings
from common.util import save_image, remove_bg, crop_vertically,upload_to_firebase_storage, delete_image
import time

async def generate_image(data:GenerateSpriteSheetDTO):



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
  
  image =  await generate_image(data=data)
  image = remove_bg(image=image)
  image = crop_vertically(image=image)
  filename = f'{str(round(time.time()))}.png'
  image_path = save_image(image=image,filename=filename)
  firebase_destination = f'assets/{data.gameId}/spritesheet/{filename}'
  firebase_url = upload_to_firebase_storage(file_path=image_path,destination_path=firebase_destination)
  delete_image(image_path=image_path)
  frame_height,frame_width,_ = image.shape
  return {"image_url":firebase_url,"frame_height":frame_height,"frame_width":frame_width//4}



