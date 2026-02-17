from app.utils import landscape, portrait, square, processbackground
from app.utils.wide import gen_wide
import os

def genbanner(json_data):
    """
    Generate banner based on size and input data
    
    Args:
        json_data: Dictionary containing banner configuration
        
    Returns:
        Path to generated banner or None if failed
    """
    try:
        from app.config.settings import Config
        # Ensure outputs directory exists
        os.makedirs(Config.OUTPUTS_FOLDER, exist_ok=True)
        
        print(f"Generating banner with size: {json_data.get('size')}")
        
        # Preprocess and resize background
        processbackground.preprocess_background(json_data)
        processbackground.resize_background(json_data, json_data['preprocessed_background'])
        
        # Generate banner based on size
        size = json_data.get("size")
        
        if size == "300x250":
            out_path = square.gen_square(json_data)
        elif size in ["300x600", "640x1280"]:
            out_path = portrait.gen_portrait(json_data)
        elif size in ["640x320", "660x300"]:
            out_path = landscape.gen_lanscape(json_data)
        elif size == "980x250":
            out_path = gen_wide(json_data)
        else:
            print(f"Unsupported banner size: {size}")
            return None
        
        print(f"Banner generated successfully: {out_path}")
        return out_path
        
    except Exception as e:
        print(f"Error in genbanner: {e}")
        import traceback
        traceback.print_exc()
        return None
    
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