import os
import cv2
import numpy as np
import base64
from app.utils.openai_client import client


def preprocess_background(json_data):
    has_bg = bool(json_data.get('background'))
    if not has_bg:
        gen_background_logo(json_data)
    else:
        gen_background(json_data)

def gen_background(json_data):
    prompt = """You were given a background image, 
You have to create a new background which using the patterns from the given background. 
NOTICE: NOT ADD ANY image or text into the image.
"""
    if json_data["size"] in ["300x600", "640x1280"]:
        size="1024x1536"
    elif json_data["size"] in ["640x320", "660x300"]:
        size="1536x1024"
    elif json_data["size"] == "300x250":
        size="1024x1024"
    elif json_data["size"] == "980x250":
        size="1536x1024"

    result = client.images.edit(
    model="gpt-image-1",
    image=[open("images/background.jpg", "rb")],
    prompt=prompt,
    size= size,
)

    image_data = result.data[0].b64_json
    image_bytes = base64.b64decode(image_data)
    out_path = f"outputs/preprocessed_background{size}.png"
    with open(out_path, "wb") as f:
        f.write(image_bytes)

    json_data['preprocessed_background'] = out_path
    
    return image_data

def gen_background_logo(json_data):
    prompt = """This is the logo image. Please create a background image with a color tone that matches with it. 
    The background image should be a single color from top to bottom, without hard edge textures. 
    Note: ONLY CREATE THE BACKGROUND IMAGE without inserting anything into it."""

    if json_data["size"] in ["300x600", "640x1280"]:
        size="1024x1536"
    elif json_data["size"] in ["640x320", "660x300"]:
        size="1536x1024"
    elif json_data["size"] == "300x250":
        size="1024x1024"
    elif json_data["size"] == "980x250":
        size="1536x1024"
            
    result = client.images.edit(
        model="gpt-image-1",
        image=[
            open(json_data["logo"], "rb"),
        ],
        prompt=prompt,
        size=size, # 1024x1024 (square) 1536x1024 (landscape) 1024x1536 (portrait)
    )
    
    image_data = result.data[0].b64_json
    image_bytes = base64.b64decode(image_data)
    out_path = f"outputs/preprocessed_background{size}.png"
    with open(out_path, "wb") as f:
        f.write(image_bytes)
    json_data['preprocessed_background'] = out_path
    
def resize_background(json_data,image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image at '{image_path}'. Check the path and file permissions.")
    size = json_data['size']
    if size== "300x250":
        cv2.imwrite(f"outputs/bg_square{size}.png",img)
    if size in ["640x320", "660x300"]:
        img = img[:768,:]
        cv2.imwrite(f"outputs/bg_landscape_l{size}.png",img[:,:768])
        cv2.imwrite(f"outputs/bg_landscape_r{size}.png",img[:,768:])
    if size in ["300x600", "640x1280"]:
        img = img[:,:710]
        cv2.imwrite(f"outputs/bg_portrait_top{size}.png",img[:1065,:])
        cv2.imwrite(f"outputs/bg_portrait_bottom{size}.png",img[1065:,:])
    if size == "980x250":
        img = img[:384,:]
        cv2.imwrite(f"outputs/bg_wide_l{size}.png", img[:,:384])
        cv2.imwrite(f"outputs/bg_wide_c{size}.png", img[:,384:384+576])
        cv2.imwrite(f"outputs/bg_wide_r{size}.png", img[:,384+576:])
        
        
    

if __name__ == "__main__":
    json_data = {
        "size": "660x300",
        "background": "images/background.jpg",
        "logo": "images/logo_samsung.png" 
    }
    preprocess_background(json_data)
    resize_background(json_data, json_data['preprocessed_background'])
    print(json_data)


