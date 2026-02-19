import uuid
import cv2
import os
import numpy as np
import base64
import shutil
from app.utils.openai_client import client

def gen_wide(json_data):
    from app.config.settings import Config
    
    size = json_data["size"]
    texts = {
        "product_name": json_data.get("product_name"),
        "product_description": json_data.get("subtext"),
        "cta": json_data.get("cta", "Mua ngay"),
        "phone": json_data.get("phone", "0123456789"),
        "discount": json_data.get("discount"),
        "website": json_data.get("website")
    }
    ## Generate center part with product image
    prompt1 = f"""This is an advertising banner. You need to place the text below into the empty areas of the banner.
    Make sure the final design maintains the original size and content of the banner.
    All text lines must be large, morden design and fill all the empty space effectively without leaving any gap.
    NOTICE: DO NOT ADD ANY IMAGE OR TEXT into the banner.
    The texts to be added are:
    Product description: {texts['product_description']}
    Product description: {texts['product_description']}
    CTA button: {texts['cta']}
    Phone: {texts['phone']}
    Discount: {texts['discount']}
    Website: {texts['website']}
    """
    result1 = client.images.edit(
        model="gpt-image-1",
        image=open(os.path.join(Config.OUTPUTS_FOLDER, f"bg_wide_c{size}.png"), "rb"),
        prompt=prompt1,
        size="1536x1024",
    )
    image_data = result1.data[0].b64_json
    image_bytes = base64.b64decode(image_data)
    with open(os.path.join(Config.OUTPUTS_FOLDER, f"banner_wide_c{size}.png"), "wb") as f:
        f.write(image_bytes)
        
    ##Generate right part with product
    prompt2 = """Generate an advertise image with given background, product image. 
The product must be cropped out and placed in the center of the banner at a large size. 
NOTICE: NOT CHANGE COLOR of the background and NOT ADD ANY new images or texts. 
"""
    # Use multiple images instead of mask to avoid size mismatch
    with open(os.path.join(Config.OUTPUTS_FOLDER, f"bg_wide_r{size}.png"), "rb") as bg_file, \
         open(json_data["product"], "rb") as product_file:
        result2 = client.images.edit(
            model="gpt-image-1",
            image=[bg_file, product_file],
            prompt=prompt2,
            size="1536x1024",
        )
    image_data = result2.data[0].b64_json
    image_bytes = base64.b64decode(image_data)
    with open(os.path.join(Config.OUTPUTS_FOLDER, f"banner_wide_r{size}.png"), "wb") as f:
        f.write(image_bytes)
        
    prompt3 = f"""
    Generate an advertise banner with given background and logo image. 
    The logo should be kept intact and have a small size but fully displayed on the top-left of the banner. 
    The banner must remain plenty of open space to put texts later.
    Make sure the final design maintains the original size and content of the banner.
    All text lines must be large, morden design and fill all the empty space effectively
    NOTICE: DO NOT ADD ANY IMAGE OR TEXT into the banner.
    The texts to be added are:
    Product name: {texts['product_name']}
    """
    # Use context manager for proper file handling
    with open(os.path.join(Config.OUTPUTS_FOLDER, f"bg_wide_l{size}.png"), "rb") as bg_file, \
         open(json_data["logo"], "rb") as logo_file:
        result3 = client.images.edit(
            model="gpt-image-1",
            image=[bg_file, logo_file],
            prompt=prompt3,
            size="1024x1024", 
        )
    image_data = result3.data[0].b64_json
    image_bytes = base64.b64decode(image_data)
    with open(os.path.join(Config.OUTPUTS_FOLDER, f"banner_wide_l{size}.png"), "wb") as f:
        f.write(image_bytes)
        
    img_left = cv2.imread(os.path.join(Config.OUTPUTS_FOLDER, f"banner_wide_l{size}.png"))
    img_center = cv2.imread(os.path.join(Config.OUTPUTS_FOLDER, f"banner_wide_c{size}.png"))
    img_right = cv2.imread(os.path.join(Config.OUTPUTS_FOLDER, f"banner_wide_r{size}.png"))
    img = cv2.hconcat([img_left, img_center, img_right])
    out_path = os.path.join(Config.OUTPUTS_FOLDER, f"banner_wide_{str(uuid.uuid4())[:8]}.png")
    cv2.imwrite(out_path, img)
    
    
    return out_path
    
        
# if __name__ == "__main__":
#     json_data = {
#         "size": "980x250",
#         "product_name": "Samsung Galaxy S23 Ultra",
#         "subtext": "The ultimate smartphone experience with cutting-edge technology and stunning design.",
#         "website": "www.samsung.com",
#         "cta": "Buy Now",
#         "discount": "20% OFF",
#         "phone": "1800-123-456",
#         "logo": "images/logo.jpg",
#         "product": "images/product.jpg"
#     }
#     gen_wide(json_data)