"""
Debug script to check database banner images
"""
from website import create_app, db
from website.models import Banner, User

app = create_app()

with app.app_context():
    print("=" * 60)
    print("DATABASE CHECK")
    print("=" * 60)
    
    # Check users
    users = User.query.all()
    print(f"\n📊 Total Users: {len(users)}")
    for user in users:
        print(f"  - User {user.id}: {user.username} ({user.email})")
    
    # Check banners
    banners = Banner.query.all()
    print(f"\n📊 Total Banners: {len(banners)}")
    
    if not banners:
        print("  ⚠️  No banners found in database!")
    else:
        for banner in banners:
            print(f"\n  Banner ID: {banner.id}")
            print(f"  User ID: {banner.user_id}")
            print(f"  Size: {banner.size}")
            print(f"  Company: {banner.company_name}")
            print(f"  Product: {banner.product_name}")
            print(f"  Created: {banner.date_created}")
            
            # Check image data
            if banner.banner_image:
                print(f"  ✅ Banner Image: {len(banner.banner_image)} bytes")
            else:
                print(f"  ❌ Banner Image: None")
            
            if banner.background_image:
                print(f"  ✅ Background Image: {len(banner.background_image)} bytes")
            else:
                print(f"  ⚠️  Background Image: None")
            
            if banner.logo_image:
                print(f"  ✅ Logo Image: {len(banner.logo_image)} bytes")
            else:
                print(f"  ⚠️  Logo Image: None")
            
            if banner.product_image:
                print(f"  ✅ Product Image: {len(banner.product_image)} bytes")
            else:
                print(f"  ⚠️  Product Image: None")
            
            # Check paths
            print(f"  Generated Path: {banner.generated_banner_path}")
            print(f"  Background Path: {banner.background_path}")
            print(f"  Logo Path: {banner.logo_path}")
            print(f"  Product Path: {banner.product_path}")
    
    print("\n" + "=" * 60)
    print("CHECK COMPLETE")
    print("=" * 60)
