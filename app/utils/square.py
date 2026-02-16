import os
import cv2
import numpy as np
import base64
import shutil
import uuid
from app.utils.openai_client import client

def gen_square(json_data):
    size = "300x250"
    texts = {
        "product_name": json_data.get("product_name"),
        "product_description": json_data.get("subtext"),
        "cta": json_data.get("cta", "Mua ngay"),
        "phone": json_data.get("phone", "0123456789"),
        "discount": json_data.get("discount"),
        "website": json_data.get("website")
    }

    prompt = f"""
Hãy tạo một banner quảng cáo vuông với các yêu cầu sau:
- Sử dụng hình nền, logo và hình ảnh sản phẩm được cung cấp.
- Bố cục siêu đẹp.
- logo, sản phẩm và các đoạn văn bản phải được sắp xếp hợp lý để tận dụng tối đa không gian trống.
- Sản phẩm phải được hiển thị đầy đủ và rõ ràng.
- các đoạn văn bản sau phải được thêm vào banner:
Tên sản phẩm: {texts['product_name']}
Mô tả sản phẩm: {texts['product_description']}
CTA: {texts['cta']}
Số điện thoại: {texts['phone']}
Khuyến mãi: {texts['discount']}
Website: {texts['website']}

"""
    result = client.images.edit(
        model="gpt-image-1",
        image=open(f"outputs/bg_square{size}.png", "rb"),
        mask=[
            open(json_data["logo"], "rb"),
            open(json_data["product"], "rb"),
        ],
        prompt=prompt,
        size="1024x1024",
    )
    image_data = result.data[0].b64_json
    image_bytes = base64.b64decode(image_data)

    os.makedirs("outputs", exist_ok=True)
    out_path = os.path.join("outputs", f"banner_square_{uuid.uuid4().hex}.png")
    with open(out_path, "wb") as f:
        f.write(image_bytes)

    return out_path

# if __name__ == "__main__":
#     json_data = {
#         "size": "300x250",
#         "product_name": "Samsung Galaxy S23 Ultra",
#         "subtext": "The ultimate smartphone experience with cutting-edge technology and stunning design.",
#         "website": "www.samsung.com",
#         "cta": "Buy Now",
#         "discount": "20% OFF",
#         "phone": "1800-123-456",
#         "background" : "images/background.jpg",
#         "logo": "images/logo.jpg",
#         "product": "images/product.jpg"
#     }
#     gen_square(json_data)
    
