import os
import cv2
import numpy as np
import base64
from app.utils.openai_client import client


def preprocess_background(json_data):
    """Preprocess background image using OpenAI API"""
    from app.config.settings import Config
    # Ensure outputs directory exists with proper permissions
    os.makedirs(Config.OUTPUTS_FOLDER, exist_ok=True)
    
    # Set directory permissions (important for server environments)
    try:
        os.chmod(Config.OUTPUTS_FOLDER, 0o755)
    except Exception as e:
        print(f"Warning: Could not set permissions on outputs folder: {e}")
    
    has_bg = bool(json_data.get('background'))
    if not has_bg:
        gen_background_logo(json_data)
    else:
        gen_background(json_data)

def gen_background(json_data):
    """Generate background from existing background image"""
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

    # Use actual uploaded background file
    background_path = json_data.get('background')
    if not background_path or not os.path.exists(background_path):
        raise FileNotFoundError(f"Background image not found: {background_path}")
    
    print(f"Processing background: {background_path}")
    
    # Verify file exists and is readable
    if not os.path.isfile(background_path):
        raise FileNotFoundError(f"Background file does not exist: {background_path}")
    
    # Check file size
    file_size = os.path.getsize(background_path)
    print(f"Background file size: {file_size} bytes")
    
    try:
        # Open file properly with context manager
        with open(background_path, "rb") as image_file:
            result = client.images.edit(
                model="gpt-image-1",
                image=image_file,
                prompt=prompt,
                size=size,
            )

        from app.config.settings import Config
        image_data = result.data[0].b64_json
        image_bytes = base64.b64decode(image_data)
        out_path = os.path.join(Config.OUTPUTS_FOLDER, f"preprocessed_background{size}.png")
        with open(out_path, "wb") as f:
            f.write(image_bytes)

        json_data['preprocessed_background'] = out_path
        print(f"Background processed successfully: {out_path}")
        
        return image_data
    except Exception as e:
        print(f"Error generating background: {e}")
        raise

def gen_background_logo(json_data):
    """Generate background from logo when no background provided"""
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
    
    # Use actual uploaded logo file
    logo_path = json_data.get('logo')
    if not logo_path or not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo image not found: {logo_path}")
    
    print(f"Generating background from logo: {logo_path}")
    
    # Verify file exists and is readable
    if not os.path.isfile(logo_path):
        raise FileNotFoundError(f"Logo file does not exist: {logo_path}")
    
    # Check file size
    file_size = os.path.getsize(logo_path)
    print(f"Logo file size: {file_size} bytes")
    
    try:
        # Open file properly with context manager
        with open(logo_path, "rb") as image_file:
            result = client.images.edit(
                model="gpt-image-1",
                image=image_file,
                prompt=prompt,
                size=size,
            )
        
        from app.config.settings import Config
        image_data = result.data[0].b64_json
        image_bytes = base64.b64decode(image_data)
        out_path = os.path.join(Config.OUTPUTS_FOLDER, f"preprocessed_background{size}.png")
        with open(out_path, "wb") as f:
            f.write(image_bytes)
        json_data['preprocessed_background'] = out_path
        print(f"Background generated successfully: {out_path}")
    except Exception as e:
        print(f"Error generating background from logo: {e}")
        raise
    
def resize_background(json_data, image_path):
    """Resize and split background image for banner composition"""
    from app.config.settings import Config
    # Ensure outputs directory exists
    os.makedirs(Config.OUTPUTS_FOLDER, exist_ok=True)
    
    print(f"Resizing background: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image at '{image_path}'. Check the path and file permissions.")
    
    from app.config.settings import Config
    size = json_data['size']
    try:
        if size == "300x250":
            cv2.imwrite(os.path.join(Config.OUTPUTS_FOLDER, f"bg_square{size}.png"), img)
        if size in ["640x320", "660x300"]:
            img = img[:768, :]
            cv2.imwrite(os.path.join(Config.OUTPUTS_FOLDER, f"bg_landscape_l{size}.png"), img[:, :768])
            cv2.imwrite(os.path.join(Config.OUTPUTS_FOLDER, f"bg_landscape_r{size}.png"), img[:, 768:])
        if size in ["300x600", "640x1280"]:
            img = img[:, :710]
            cv2.imwrite(os.path.join(Config.OUTPUTS_FOLDER, f"bg_portrait_top{size}.png"), img[:1065, :])
            cv2.imwrite(os.path.join(Config.OUTPUTS_FOLDER, f"bg_portrait_bottom{size}.png"), img[1065:, :])
        if size == "980x250":
            img = img[:384, :]
            cv2.imwrite(os.path.join(Config.OUTPUTS_FOLDER, f"bg_wide_l{size}.png"), img[:, :384])
            cv2.imwrite(os.path.join(Config.OUTPUTS_FOLDER, f"bg_wide_c{size}.png"), img[:, 384:384+576])
            cv2.imwrite(os.path.join(Config.OUTPUTS_FOLDER, f"bg_wide_r{size}.png"), img[:, 384+576:])
        print(f"Background resized successfully for size: {size}")
    except Exception as e:
        print(f"Error resizing background: {e}")
        raise
        
        
    

# if __name__ == "__main__":
#     json_data = {
#         "size": "660x300",
#         "background": "images/background.jpg",
#         "logo": "images/logo_samsung.png" 
#     }
#     preprocess_background(json_data)
#     resize_background(json_data, json_data['preprocessed_background'])
#     print(json_data)


