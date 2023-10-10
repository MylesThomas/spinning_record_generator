# Animated Spinning Record GIF Generator

## Transloadit Signup

This project will leverage Transloadit, a media processing service.

According to [https://transloadit.com/](https://transloadit.com/), "Transloadit is the world's most advanced file uploading and processing service aimed at developers. Our API is an all-in-one tool for your users' files."

Let's start by heading to [Transloadit Sign Up Page](https://transloadit.com/c/signup/) to sign up.
-  I logged in via Github to streamline the process

Upon logging in, you will be prompted to Create an App. Name your app anything you like, such as "Vinyl GIF Generator"

From there, look to your left-hand side and head to the Templates page, and click on 'Create my first Template'.
- I created an empty template

Paste the following JSON code into your Template:

```json
{
  "steps": {
    ":original": {
      "robot": "/upload/handle"
    },
    "resize": {
      "use": ":original",
      "robot": "/image/resize",
      "format": "png",
      "resize_strategy": "fillcrop",
      "width": 350,
      "height": 350,
      "imagemagick_stack": "v2.0.7"
    }
  }
}
```

Quick explanation of this code:
- `:original`: handles uploading our input file.
- `resize`: handles cropping our image and sets the format to PNG.
  - 
- ``: 
- ``: 
- ``: 
- ``: 
- ``: 
- ``: 



Note: Creating a template 'Via the Wizard' can work too.

## Project Setup

Setup the local directory:

```sh
mkdir spinning_record_generator
cd spinning_record_generator
```

Head to [Github](github.com) and create a new repository named `spinning_record_generator`.

Next, create a new Git repository from the command line:

```sh
echo "# spinning_record_generator" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/MylesThomas/spinning_record_generator.git
git push -u origin main
```

Save this file into the root directory as a markdown file named `spinning_record_generator_notes.md`.

Next, setup a virtual Python environment:

```sh
cd spinning_record_generator
py -m venv env
```

You should now see a folder 'env' with a python.exe program in the /Scripts directory.

Create a .gitignore file for the Python project and save it in the root directory `spinning_record_generator`:

```sh
cd spinning_record_generator
echo > .gitignore
```

Code for the .gitignore file: [Link to .gitignore template](https://github.com/github/gitignore/blob/main/Python.gitignore)

Next, activate the virtual environment in the terminal:

```sh
where python
.\env\Scripts\activate

python.exe -m pip install --upgrade pip
pip list
```

Note: You can leave the virtual environment with this call:

```sh
deactivate
```

Next, install the necessary packages into your virtual environment:

```sh
pip install pytransloadit
pip install numpy
pip install opencv-python
pip install requests
pip install future
```

## Other Prerequisites

Coupled with our packages, we need some Assets/photos to use. Create a folder named `Assets`:

```sh
mkdir Assets
```

Next, download these files and save them as `vinyl.png` and `okcomputer.jpg`, respectively.

- [vinyl.png](https://raw.githubusercontent.com/Missing-Tech/Vinyl-Gif-Maker/main/.github/images/vinyl.png)

- [okcomputer.jpg](https://raw.githubusercontent.com/Missing-Tech/Vinyl-Gif-Maker/main/.github/images/okcomputer.jpg)

Now that we have our project nearly setup, we can start coding. First we will create a python file:

```sh
echo > spinning_vinyl.py
```

Note: I am using VSCode, but any text editor should work.

At the top of the project, let's add the following imports:

```py
# IMPORTS
from __future__ import print_function
from transloadit import client
import os
import requests
import cv2
import numpy as np
```

Make sure to also create a transloadit client, like this:

```py
# CREATE TRANSLOADIT CLIENT
TRANSLOADIT_KEY = "02da89521b8342349835e949728cea33"
TRANSLOADIT_SECRET = "f1ab67738c9e9fd1266a457c06fbb05a990c43c6"
tl = client.Transloadit(TRANSLOADIT_KEY, TRANSLOADIT_SECRET)
```

Note: You can find TRANSLOADIT_KEY and TRANSLOADIT_SECRET in vinyl-gif-generator/Credentials.

Before we can start making our first template, let's create a set of global variables for use later. Make sure of the following:
- img_name: match the file name, remove the file extension (e.g. `.jpg`/`.png`)
- vinyl_path: match the name of the vinyl record image (Before, we saved it as `vinyl.png`)

```py
# GLOBAL VARIABLES
img_name = 'okcomputer'
img_path = f"Assets/{img_name}.jpg"
vinyl_path = 'Assets/vinyl.png'
remove_bg_location = 'Assets/trimmed_image.png'
```

Note: I am not entirely sure what `remove_bg_location` is there for, but let's proceed for now.

Now we are all set to make our first Template!

---

## Templates

### Making a Template

Head to your Transloadit console and create a blank Template. Make sure to note down your Template ID for later. Below, we have copied over our Template code, which is simply the JSON recipe to create your Transloadit magic. We'll run through each Step below and explain what's going on.

```py
# template name: template1
# template id: 4fad01b9ccac4b288bc6f27d6c9d3ca1
{
  "steps": {
    ":original": {
      "robot": "/upload/handle"
    },
    "resize": {
      "use": ":original",
      "robot": "/image/resize",
      "format": "png",
      "resize_strategy": "fillcrop",
      "width": 350,
      "height": 350,
      "imagemagick_stack": "v3.0.0"
    }
  }
}

```

Note: "imagemagick_stack": "v3.0.0" used to be "imagemagick_stack": "v2.0.7"

### Using our Templates

Since we are using multiple Templates, we need to create a small Python script to link them to each other. We will accomplish this by parsing our first Template's Assembly result, then taking the resulted temporary URL value and passing it onto our second Template.

The function below is passed our previously-noted Template ID, our image's file path, and the name of the last Step in our Template (for our example, it would be `resize`). It also contains a few optional parameters, like whether or not we want to return the URL and, most importantly, `fields`. Using fields, we can pass variables into our Template so we can change the parameters of our Template straight from our client.

```py
def useTemplate(templateID, file_path='', result_name='', get_url=True, fields=''):
    assembly = tl.new_assembly({'template_id': templateID, 'fields': fields})

    if file_path != '':
        assembly.add_file(open(file_path, 'rb'))

    assembly_response = assembly.create(retries=5, wait=True)
    if get_url:
        assembly_url = assembly_response.data.get('results').get(result_name)[0].get('ssl_url')
        return assembly_url
```

We also need to create one more utility function to download our resized image to the `./Assets/` folder.

```py
def downloadImage(url, location):
    r = requests.get(url)
    image = open(location, 'wb')
    image.write(r.content)
    image.close()
```

### Removing the background

This Template is straightforward; it enables the alpha channel on our PNG image, then sets all black pixels as transparent. However, this also means that we have to be careful when we're using album art with a black background - such as the [Dark Side of the Moon by Pink Floyd](https://github.com/Missing-Tech/Vinyl-Gif-Maker/blob/main/.github/images/darkside.gif).

```py
# template name: template2
# template id: 3a650cf58e524bd4a79d531c2db5ea48
{
  "steps": {
    ":original": {
      "robot": "/upload/handle"
    },
    "trimmed": {
      "use": ":original",
      "robot": "/image/resize",
      "alpha": "Activate",
      "type": "TrueColor",
      "transparent": "0,0,0",
      "imagemagick_stack": "v3.0.0"
    }
  }
}

```

### Overlaying the image

Now for some fields magic. We're going to take the URL of the image from our last Assembly and pass that in as a field into our Template. The `/image/resize` Robot will use the image as a watermark to overlay it on top of our vinyl record.

```py
# template name: template3
# template id: 81c576956f964c6d8d1293b9dbaa4c50
{
  "steps": {
    ":original": {
      "robot": "/upload/handle"
    },
    "watermark": {
      "use": ":original",
      "robot": "/image/resize",
      "watermark_url": "${fields.url}",
      "watermark_size": "33%",
      "watermark_position": "center",
      "imagemagick_stack": "v3.0.0"
    }
  }
}

```

Note: If you'd like to increase the size of the overlayed image, go into template3 on [transloadit.com](transloadit.com), then change "watermark_size" from 33% to ~40%.

### Turning it into a GIF!

This is our last Template. It might look daunting, but it's pretty simple when you break it down.

```py
# template name: template4
# template id: 711db6acd5f94f538d4648ef25cbff74
{
  "steps": {
    "import": {
      "robot": "/http/import",
      "url": "${fields.url}",
      "result": true
    },
    "animated": {
      "robot": "/video/merge",
      "use": "import",
      "result": true,
      "duration": "${fields.duration}",
      "framerate": "${fields.framerate}",
      "ffmpeg_stack": "v4.3.1",
      "ffmpeg": {
        "vf": "rotate=3.1415926535898*t:c=white@0, loop = -1",
        "f": "gif",
        "pix_fmt": "rgb24"
      }
    }
  }
}

```

The first Step `import` is used to, well, import our file. We use our `/http/import` Robot to bypass downloading our image from the previous Assembly locally. This requires a URL to import from. Luckily, we can easily use the field we made to pass a URL from our Python script.

Now, this is where we use FFmpeg to create our desired spinning effect. We use the rotate video flag on the overlayed image, setting it to pi multiplied by our current frame number `t`. By appending `c:white@0`, we can set the background color on our gif to white. Lastly, `loop=-1` will infinitely loop our GIF, finalising our vinyl record animation.

### Tying it all together in Python

Now we should have all the pieces we need to make our spinning vinyl GIF!

Let's start by resizing the image and downloading it locally:

```py
RESIZE_IMAGE_TEMPLATE_ID = "4fad01b9ccac4b288bc6f27d6c9d3ca1"
resize_url = useTemplate([RESIZE_IMAGE_TEMPLATE_ID], img_path, 'resize')
resized_image_location = 'Assets/resized_image.png'
downloadImage(resize_url, resized_image_location)

```

Next, we need to make our image masking function. Let's call it `maskImage` and give it an `img_path`.

```py
def maskImage(img_path):
    img = cv2.imread(img_path)
    mask = np.zeros(img.shape, dtype=np.uint8)
    size_of_image = 175 # default value: 175 (i thought this was a bit small...)
    size_of_small_hole = 20
    mask = cv2.circle(mask, (175, 175), size_of_image, (255, 255, 255), -1)
    mask = cv2.circle(mask, (175, 175), size_of_small_hole, (0, 0, 0), -1)
    result = cv2.bitwise_and(img, mask)

    result_location = 'Assets/mask.png'
    cv2.imwrite(result_location, result)

    REMOVING_BG_TEMPLATE_ID = "3a650cf58e524bd4a79d531c2db5ea48"
    remove_bg_url = useTemplate([REMOVING_BG_TEMPLATE_ID], result_location, 'trimmed')
    downloadImage(remove_bg_url, remove_bg_location)
    return remove_bg_url

```

The beginning of our function creates a black image with the exact same dimensions as our album art and then creates two white circles to produce a donut, like so:

[Donut BEFORE bitwise operation]()

We now perform a bitwise AND operation on both the mask and our original image, meaning that a pixel from the original image is only shown in places where the mask has a white pixel - giving us the following result:

[Donut AFTER bitwise operation]()

Finally, we use our earlier Template to make the black pixels transparent.

[Black Pixels == Transparent]()

We call our function like so:

```py
trimmed_url = maskImage(resized_image_location)

```

Now we need to put our donut on the vinyl record and make it spin! Let's watermark the image using our Template from before:

```py
finished_watermarked_location = 'Assets/vinyl_finished.png'
WATERMARK_IMAGE_TEMPLATE_ID = "81c576956f964c6d8d1293b9dbaa4c50"
vinyl_url = useTemplate([WATERMARK_IMAGE_TEMPLATE_ID], vinyl_path, 'watermark', True, {'url': trimmed_url})
```

[Finished Vinyl BEFORE spinning]()

Now, by passing the still image onto our GIF-generating Template along with a framerate and length, which we define from our script, we can make it spin!

```py
frame_rate = 60
length = 2

ROTATING_GIF_TEMPLATE_ID = "711db6acd5f94f538d4648ef25cbff74"
final_gif_url = useTemplate([ROTATING_GIF_TEMPLATE_ID],
                            result_name='animated',
                            get_url=True,
                            fields={'url': vinyl_url, 'duration': length, 'framerate': frame_rate})

```

Finally, we can download the result locally.

```py
final_gif_location = 'Assets/finished_gif.gif'
downloadImage(final_gif_url, final_gif_location)
```

Run the code locally on your computer:

```sh
python spinning_vinyl.py
```

And there, at last, we have it: our very own animated spinning vinyl record!

[Finished Vinyl BEFORE spinning]()

### How to perform this operation with a different image

Steps:
1. Open 'okcomputer.png' in Paint
2. Copy/Paste a new image over it
3. Save
4. Run the code for `spinning_vinyl.py`
5. Open the new .gif at Assets/finished_gif.gif

### Turning the .gif into a .png (for Soundcloud)

You can turn the .gif into a .png using a site [like this](https://cloudconvert.com/gif-to-png).

---

## References

- [Joseph Grabski - Let's Build: Animated Spinning Record GIF Generator (Tansloadit)](https://transloadit.com/blog/2021/04/vinyl-gif/)
- [Github Repository](https://github.com/Missing-Tech/Vinyl-Gif-Maker/tree/main)