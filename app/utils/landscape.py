import uuid
import cv2
import os
import numpy as np
import base64
import shutil
from app.utils.openai_client import client


def gen_lanscape(json_data):
    size = json_data["size"]
    texts = {
        "product_name": json_data.get("product_name"),
        "product_description": json_data.get("subtext"),
        "cta": json_data.get("cta", "Mua ngay"),
        "phone": json_data.get("phone", "0123456789"),
        "discount": json_data.get("discount"),
        "website": json_data.get("website")
    }

    prompt1 = """Generate an advertise image with given background, product image. 
The product must be cropped out and placed in the center of the banner at a large size. 
NOTICE: NOT CHANGE COLOR of the background and NOT ADD ANY new images or texts. 
"""

    result1 = client.images.edit(
    model="gpt-image-1",
    image=[
         open(f"outputs/bg_landscape_r{size}.png", "rb"),
         open(json_data["product"], "rb"),
         ],
    prompt=prompt1,
    size="1024x1024",
)
    image_data = result1.data[0].b64_json
    image_bytes = base64.b64decode(image_data)
    with open(f"outputs/banner_landscape_r{size}.png", "wb") as f:
        f.write(image_bytes)
    
    prompt2 = f"""
    Generate an advertise banner with given background and logo image. 
    The logo should be kept intact and have a small size but fully displayed on the top-left of the banner. 
    The banner must remain plenty of open space to put texts later.
    You have to place the text below into the banner BUT NOT CHANGE ANY from original banner.
    All text lines must be large, morden design and fill all the empty space effectively without leaving any gap.
    NOTICE: DO NOT ADD ANY new images or texts.Padding the edges of the banner 20px
    The texts to be added are:
    Product name: {texts['product_name']}
    Product description: {texts['product_description']}
    CTA button: {texts['cta']}
    Phone: {texts['phone']}
    Discount: {texts['discount']}
    Website: {texts['website']}
    """
    
    result2 = client.images.edit(
    model="gpt-image-1",
    image=[
         open(f"outputs/bg_landscape_l{size}.png", "rb"),
         open(json_data["logo"], "rb"),
         ],
    prompt=prompt2,
    size="1024x1024",
)
    image_data = result2.data[0].b64_json
    image_bytes = base64.b64decode(image_data)
    with open(f"outputs/banner_landscape_l{size}.png", "wb") as f:
        f.write(image_bytes)
        
    img_left = cv2.imread(f"outputs/banner_landscape_l{size}.png")
    img_right = cv2.imread(f"outputs/banner_landscape_r{size}.png")
    if img_left is None or img_right is None:
        raise FileNotFoundError("Không tìm thấy file ảnh hoặc file bị lỗi!")
    
    img = cv2.hconcat([img_left, img_right])
    out_path = f"outputs/banner_landscape_{uuid.uuid4().hex}.png"
    cv2.imwrite(out_path, img)
    
    return out_path
    
    
        
# if __name__ == "__main__":
#     json_data = {
#         "size": "660x300",
#         "product_name": "iPhone 17 Pro Max",
#         "subtext": "The ultimate smartphone experience with cutting-edge technology and stunning design.",
#         "website": "www.apple.com",
#         "cta": "Buy Now",
#         "discount": "20% OFF",
#         "phone": "1800-123-456",
#         "logo": "images/logo-apple.png",
#         "product": "images/IP_17_Pro_Max_Cam.png"
#     }
#     gen_lanscape(json_data)
    