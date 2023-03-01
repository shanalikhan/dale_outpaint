import openai
import os
import cv2
import numpy as np
from PIL import Image
import wget

os.environ['OPENAI_API_KEY'] = 'xxx'
#openai.organization = "Personal"
openai.api_key = 'xxx'




## Taking Input image and converting to RGBA and standard 1024 * 1024 Open AI image
## TODO : We need to use DALE to generate this image as well.

input_image = cv2.imread('perspective.jpg')

input_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2RGBA)


input_image = cv2.resize(input_image, (1024, 1024),
               interpolation = cv2.INTER_LINEAR)

## Saving this image to use further
cv2.imwrite('source.png',input_image)

# Converting image into three chunks

chunk_width = int(input_image.shape[1]/3)

# Storing the first chunk
first_chunk = input_image[:,0:chunk_width:,]

# Second and third chunk
partial_image = input_image[:,chunk_width:1024,]

# Adding mask as new chunk and merging into 2nd and 3rd chunk and saving it
last_chunk_image = np.zeros((1024,chunk_width,4))
out_image_new = np.concatenate((partial_image,last_chunk_image),axis=1)
out_image_new[chunk_width:,:3] = 0
cv2.imwrite('partial.png',out_image_new)


# Sending it to OPEN AI to fill mask image

response = openai.Image.create_edit(
  image=open("partial.png", "rb"),
  mask=open("partial.png", "rb"),
  prompt="man running towards other man who is sitting on chair",
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']

# Downloading image
import requests
image_req = requests.get(image_url)

open("1.png", "wb").write(image_req.content)



# Merging first chunk to output image
second_part = cv2.imread('1.png')
second_part = cv2.cvtColor(second_part, cv2.COLOR_RGB2RGBA)
final_image = np.concatenate((first_chunk,second_part),axis=1)
cv2.imwrite('output.png',final_image)


### Staring Second Transformation


final_image = cv2.imread('output.png')
final_image = cv2.cvtColor(final_image, cv2.COLOR_RGB2RGBA)
final_image_chunk_size = int(final_image.shape[1]/2)

# Storing the first chunk
pre_chunk = final_image[:,0:final_image_chunk_size:,]

# Second chunk
post_chunk = final_image[:,final_image_chunk_size:final_image.shape[1],]
last_chunk_image = np.zeros((1024,1023-final_image_chunk_size,4))
out_image_new = np.concatenate((post_chunk,last_chunk_image),axis=1)
out_image_new[final_image_chunk_size:,:3] = 0
cv2.imwrite('partial.png',out_image_new)


response = openai.Image.create_edit(
  image=open("partial.png", "rb"),
  mask=open("partial.png", "rb"),
  prompt="raining and wind blowing",
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']

# Downloading image
import requests
image_req = requests.get(image_url)

open("2.png", "wb").write(image_req.content)
# Merging first chunk to output image
second_part = cv2.imread('2.png')
second_part = cv2.cvtColor(second_part, cv2.COLOR_RGB2RGBA)
final_image = np.concatenate((pre_chunk,second_part),axis=1)
cv2.imwrite('output.png',final_image)



