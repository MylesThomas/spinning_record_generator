# IMPORTS 
from __future__ import print_function
from transloadit import client
import os
import requests
import cv2
import numpy as np

# CREATE TRANSLOADIT CLIENT
TRANSLOADIT_KEY = "02da89521b8342349835e949728cea33"
TRANSLOADIT_SECRET = "f1ab67738c9e9fd1266a457c06fbb05a990c43c6"
tl = client.Transloadit(TRANSLOADIT_KEY, TRANSLOADIT_SECRET)

# GLOBAL VARIABLES
img_name = 'okcomputer'
img_path = f"Assets/{img_name}.jpg"
vinyl_path = 'Assets/vinyl.png'
remove_bg_location = 'Assets/trimmed_image.png'

# utility function
def useTemplate(templateID, file_path='', result_name='', get_url=True, fields=''):
    assembly = tl.new_assembly({'template_id': templateID, 'fields': fields})

    if file_path != '':
        assembly.add_file(open(file_path, 'rb'))

    assembly_response = assembly.create(retries=5, wait=True)
    if get_url:
        assembly_url = assembly_response.data.get('results').get(result_name)[0].get('ssl_url')
        return assembly_url

# utility function (to download our resized image to the `./Assets/` folder)
def downloadImage(url, location):
    r = requests.get(url)
    image = open(location, 'wb')
    image.write(r.content)
    image.close()

# BEGIN LOGIC

# Let's start by resizing the image and downloading it locally:
RESIZE_IMAGE_TEMPLATE_ID = "4fad01b9ccac4b288bc6f27d6c9d3ca1"
resize_url = useTemplate([RESIZE_IMAGE_TEMPLATE_ID], img_path, 'resize')
resized_image_location = 'Assets/resized_image.png'
downloadImage(resize_url, resized_image_location)

# Next, we need to make our image masking function. Let's call it `maskImage` and give it an `img_path`.
def maskImage(img_path):
    img = cv2.imread(img_path)
    mask = np.zeros(img.shape, dtype=np.uint8)
    
    radius_of_image = 175 # default value: 175 (i thought this was a bit small...)
    center_coordinates = (radius_of_image, radius_of_image)
    radius_of_small_hole = 20
    
    color_1 = (255, 255, 255)
    color_2 = (0, 0, 0)
    thickness_border = -1
    
    mask = cv2.circle(mask, center_coordinates, radius_of_image, color_1, thickness_border) # 255 = white
    mask = cv2.circle(mask, center_coordinates, radius_of_small_hole, color_2, thickness_border) # 0 = black
    
    result = cv2.bitwise_and(img, mask)

    result_location = 'Assets/mask.png'
    cv2.imwrite(result_location, result)

    REMOVING_BG_TEMPLATE_ID = "3a650cf58e524bd4a79d531c2db5ea48"
    remove_bg_url = useTemplate([REMOVING_BG_TEMPLATE_ID], result_location, 'trimmed')
    downloadImage(remove_bg_url, remove_bg_location)
    return remove_bg_url

# Finally, we use our earlier Template to make the black pixels transparent.
trimmed_url = maskImage(resized_image_location)

# Now we need to put our donut on the vinyl record and make it spin! Let's watermark the image using our Template from before:
finished_watermarked_location = 'Assets/vinyl_finished.png'
WATERMARK_IMAGE_TEMPLATE_ID = "81c576956f964c6d8d1293b9dbaa4c50"
vinyl_url = useTemplate([WATERMARK_IMAGE_TEMPLATE_ID], vinyl_path, 'watermark', True, {'url': trimmed_url})

# Now, by passing the still image onto our GIF-generating Template along with a framerate and length, which we define from our script, we can make it spin!
frame_rate = 60
length = 2

ROTATING_GIF_TEMPLATE_ID = "711db6acd5f94f538d4648ef25cbff74"
final_gif_url = useTemplate([ROTATING_GIF_TEMPLATE_ID],
                            result_name='animated',
                            get_url=True,
                            fields={'url': vinyl_url, 'duration': length, 'framerate': frame_rate})

# Finally, we can download the result locally.
final_gif_location = 'Assets/finished_gif.gif'
downloadImage(final_gif_url, final_gif_location)

# DONE!
print(f"Done! You can find the .gif at Assets/finished_gif.gif")