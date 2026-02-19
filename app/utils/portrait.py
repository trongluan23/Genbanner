import uuid
import cv2
import os
import numpy as np
import base64
import shutil
from app.utils.openai_client import client

def gen_portrait(json_data):
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
     
    prompt1 = f"""Hãy tạo banner quảng cáo với các yêu cầu sau:
    - Sử dụng hình nên được cung cấp 
    - Hãy thêm các văn bản dưới đây để lắp đầy tối đa không gian trống của banner.:
    Tuyệt đối : Không tạo thêm bât kỳ hình ảnh, văn bản hay logo nào khác 
    - Mổ tả: {texts['product_description']}
    - CTA: {texts['cta']}
    - Phone: {texts['phone']}
    - Discount: {texts['discount']}
    - Website: {texts['website']}
    """

    result1 = client.images.edit(
        model="gpt-image-1",
        image=open(os.path.join(Config.OUTPUTS_FOLDER, f"bg_portrait_bottom{size}.png"), "rb"),
        prompt=prompt1,
        size="1536x1024",
    )
    image_data = result1.data[0].b64_json
    image_bytes = base64.b64decode(image_data)
    temp_bot_path = os.path.join(Config.OUTPUTS_FOLDER, "banner_portrait_bot_temp.png")
    with open(temp_bot_path, "wb") as f:
        f.write(image_bytes)
    
    prompt2 = f"""
    Hãy tạo phần trên của banner quảng cáo dọc với các yêu cầu sau:
    - Sử dụng hình nền, logo và hình ảnh sản phẩm được cung cấp.
    - Bố cục siêu đẹp.
    - logo, sản phẩm và các đoạn văn bản phải được sắp xếp hợp lý để tận dụng tối đa không gian trống.
    - Sản phẩm phải được hiển thị đầy đủ và rõ ràng, nằm gọn trong khung banner, tuyệt đối không bị cắt xén.
    - Chỉ thêm đoạn văn bản sau vào banner:
    - Không tạo thêm bất kỳ văn bản và hình ảnh nào khác
    Tên sản phẩm: {texts['product_name']}
    """
    
    # Use context manager for proper file handling
    with open(os.path.join(Config.OUTPUTS_FOLDER, f"bg_portrait_top{size}.png"), "rb") as bg_file, \
         open(json_data["logo"], "rb") as logo_file, \
         open(json_data["product"], "rb") as product_file:
        result2 = client.images.edit(
            model="gpt-image-1",
            image=[bg_file, logo_file, product_file],
            prompt=prompt2,
            size="1024x1536",
        )
    image_data = result2.data[0].b64_json
    image_bytes = base64.b64decode(image_data)
    temp_top_path = os.path.join(Config.OUTPUTS_FOLDER, "banner_portrait_top_temp.png")
    with open(temp_top_path, "wb") as f:
        f.write(image_bytes)
        
    img_top = cv2.imread(temp_top_path)
    img_bot = cv2.imread(temp_bot_path)
    img_bot = cv2.resize(img_bot, (1024, 682))  # Resize to desired dimensions
    if img_top is None or img_bot is None:
        raise FileNotFoundError("Không tìm thấy file ảnh hoặc file bị lỗi!")

    img = cv2.vconcat([img_top, img_bot])
    img = cv2.resize(img, (1024, 2048))  # Resize to desired dimensions
    
    # Save to outputs folder with unique filename
    os.makedirs(Config.OUTPUTS_FOLDER, exist_ok=True)
    out_path = os.path.join(Config.OUTPUTS_FOLDER, f"banner_portrait_{uuid.uuid4().hex}.png")
    cv2.imwrite(out_path, img)
    
    # Clean up temporary files
    try:
        if os.path.exists(temp_top_path):
            os.remove(temp_top_path)
        if os.path.exists(temp_bot_path):
            os.remove(temp_bot_path)
    except:
        pass  # Ignore cleanup errors
    
    return out_path
        
        
# if __name__ == "__main__":
#     json_data = {
#         "size": "300x600",
#         "product_name": "iPhone 17 Pro Max",
#         "subtext": "The ultimate smartphone experience with cutting-edge technology and stunning design.",
#         "website": "www.apple.com",
#         "cta": "Buy Now",
#         "discount": "20% OFF",
#         "phone": "1800-123-456",
#         "background" : "images/background.png",
#         "logo": "images/logo-apple.png",
#         "product": "images/IP_17_Pro_Max_Cam.png"
#     }
#     gen_portrait(json_data)
        


    