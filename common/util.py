import cv2
from sklearn.cluster import KMeans
import os
from firebase_admin import storage


def find_vertical_limit(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    upper_position = next((i for i, row in enumerate(gray) if cv2.countNonZero(row) > 0), None)

    lower_position = next((i for i, row in enumerate(reversed(gray)) if cv2.countNonZero(row) > 0), None)

    if upper_position is None or lower_position is None:
        return None, None

    lower_position = image.shape[0] - lower_position - 1

    return upper_position, lower_position

def crop_vertically(image):


  upper_coordinate, lower_coordinate = find_vertical_limit(image)

  width = 128
  height = 128
  cropped_image = image[upper_coordinate:lower_coordinate, :]

  cropped_image_resized = cv2.resize(cropped_image, (width, height))

  return cropped_image_resized

def clusterize_bg(image):

  pixels = image.reshape(-1,3)

  kmeans = KMeans(n_clusters=5)

  kmeans.fit(pixels)

  labels = kmeans.labels_

  segmented_image = labels.reshape(image.shape[0], image.shape[1])


  clustered_image = image.copy()
  height, width = segmented_image.shape
  for x in range(height):
    for y in range(width):
      if segmented_image[x][y] == 0:
        clustered_image[x,y] = 0



  return clustered_image

def remove_bg(image):
  src = clusterize_bg(image)

  tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

  _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)

  b, g, r = cv2.split(src)

  rgba = [b, g, r, alpha]

  dst = cv2.merge(rgba, 4)

  return dst


def save_image(image,filename):
   if os.path.isdir("generations") == False:
      os.makedirs("generations")
   save_path = os.path.join("generations",filename)
   cv2.imwrite(save_path,image)
   return save_path

def delete_image(image_path):
  
  if not isinstance(image_path, str):
    raise ValueError("Image path must be a string.")

  try:
    
    os.remove(image_path)
    return True
  except FileNotFoundError:
    print(f"Error: Image file not found: {image_path}")
    return False


   
def upload_to_firebase_storage(file_path,destination_path):
   bucket = storage.bucket()
   blob = bucket.blob(destination_path)
   blob.upload_from_filename(file_path)
   blob.make_public()

   return blob.public_url
