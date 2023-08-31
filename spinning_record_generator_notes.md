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
- `:original`: 
- ``: 
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

Coupled with our packages, we need some assets/photos to use. Create a folder named `assets`:

```sh
mkdir assets
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
tl = client.Transloadit(TRANSLOADIT_KEY, TRANSLOADIT_SECRET)
```

Before we can start making our first template, let's create a set of global variables for use later. Make sure of the following:
- img_name: match the file name, remove the file extension (e.g. `.jpg`/`.png`)
- vinyl_path: match the name of the vinyl record image (Before, we saved it as `vinyl.png`)

```py
# GLOBAL VARIABLES
img_name = 'okcomputer'
img_path = f"assets/{img_name}.jpg"
vinyl_path = 'assets/vinyl.png'
remove_bg_location = 'assets/trimmed_image.png'
```

Note: I am not entirely sure what `remove_bg_location` is there for, but let's proceed for now.

Now we are all set to make our first Template!

---

## Templates

###

### Making a Template

In order to make a template, you want to go to your transloadit console and create a new app. Name your app anything you like, such as "Vinyl GIF Generator", then go to the templates section on the left. From here you will be creating a blank template, although Transloadit has a very helpful wizard to automatically generate a template for you! From this page, you can find your template ID which will be useful in the upcoming steps.


---

## References

- [Joseph Grabski - Let's Build: Animated Spinning Record GIF Generator (Tansloadit)](https://transloadit.com/blog/2021/04/vinyl-gif/)
- [Github Repository](https://github.com/Missing-Tech/Vinyl-Gif-Maker/tree/main)