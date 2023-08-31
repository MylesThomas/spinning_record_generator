# IMPORTS 
from __future__ import print_function
from transloadit import client
import os
import requests
import cv2
import numpy as np

# CREATE TRANSLOADIT CLIENT
tl = client.Transloadit(TRANSLOADIT_KEY, TRANSLOADIT_SECRET)

# GLOBAL VARIABLES
img_name = 'okcomputer'
img_path = f"assets/{img_name}.jpg"
vinyl_path = 'assets/vinyl.png'
remove_bg_location = 'assets/trimmed_image.png'

# 