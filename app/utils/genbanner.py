from app.utils import landscape, portrait, square, processbackground
from app.utils.wide import gen_wide

def genbanner(json_data):
    if json_data["size"] == "300x250":
        processbackground.preprocess_background(json_data)
        processbackground.resize_background(json_data, json_data['preprocessed_background'])
        out_path = square.gen_square(json_data)
    if json_data["size"] in ["300x600", "640x1280"]:
        processbackground.preprocess_background(json_data)
        processbackground.resize_background(json_data, json_data['preprocessed_background'])
        out_path = portrait.gen_portrait(json_data)
    if json_data["size"] in ["640x320", "660x300"]:
        processbackground.preprocess_background(json_data)
        processbackground.resize_background(json_data, json_data['preprocessed_background'])
        out_path = landscape.gen_lanscape(json_data)
    if json_data["size"] == "980x250":
        processbackground.preprocess_background(json_data)
        processbackground.resize_background(json_data, json_data['preprocessed_background'])
        out_path = gen_wide(json_data) 
    
    return out_path
    
# if __name__ == "__main__":
#     json_data = {
#         "size": "640x320",
#         "product_name": "Samsung Galaxy S23 Ultra",
#         "subtext": "The ultimate smartphone experience with cutting-edge technology and stunning design.",
#         "website": "www.samsung.com",
#         "cta": "Buy Now",
#         "discount": "20% OFF",
#         "phone": "1800-123-456",
#         "logo": "images/logo.jpg",
#         "product": "images/product.jpg"
#     }
#     genbanner(json_data)