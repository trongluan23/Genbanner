"""
Test script to verify MVC structure is working correctly
"""
import sys
import os

def test_imports():
    """Test if all imports work correctly"""
    print("Testing imports...")
    
    try:
        from app import create_app, db
        print("✅ app imports OK")
    except ImportError as e:
        print(f"❌ app imports FAILED: {e}")
        return False
    
    try:
        from app.models.user import User
        from app.models.banner import Banner
        print("✅ models imports OK")
    except ImportError as e:
        print(f"❌ models imports FAILED: {e}")
        return False
    
    try:
        from app.controllers.auth_controller import auth_bp
        from app.controllers.banner_controller import banner_bp
        print("✅ controllers imports OK")
    except ImportError as e:
        print(f"❌ controllers imports FAILED: {e}")
        return False
    
    try:
        from app.services.banner_service import BannerService
        from app.services.file_service import FileService
        print("✅ services imports OK")
    except ImportError as e:
        print(f"❌ services imports FAILED: {e}")
        return False
    
    try:
        from app.utils.genbanner import genbanner
        from app.utils.openai_client import client
        print("✅ utils imports OK")
    except ImportError as e:
        print(f"❌ utils imports FAILED: {e}")
        return False
    
    try:
        from app.config.settings import Config
        print("✅ config imports OK")
    except ImportError as e:
        print(f"❌ config imports FAILED: {e}")
        return False
    
    return True

def test_app_creation():
    """Test if Flask app can be created"""
    print("\nTesting app creation...")
    
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation FAILED: {e}")
        return False

def test_blueprints():
    """Test if blueprints are registered"""
    print("\nTesting blueprints...")
    
    try:
        from app import create_app
        app = create_app()
        
        blueprints = [bp.name for bp in app.blueprints.values()]
        print(f"Registered blueprints: {blueprints}")
        
        if 'auth' in blueprints and 'banner' in blueprints:
            print("✅ All blueprints registered")
            return True
        else:
            print("❌ Missing blueprints")
            return False
    except Exception as e:
        print(f"❌ Blueprint test FAILED: {e}")
        return False

def test_routes():
    """Test if routes are accessible"""
    print("\nTesting routes...")
    
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test home route
            response = client.get('/')
            print(f"GET / → Status: {response.status_code}")
            
            # Test login route
            response = client.get('/auth/login')
            print(f"GET /auth/login → Status: {response.status_code}")
            
            # Test register route
            response = client.get('/auth/register')
            print(f"GET /auth/register → Status: {response.status_code}")
            
            print("✅ Routes accessible")
            return True
    except Exception as e:
        print(f"❌ Routes test FAILED: {e}")
        return False

def test_database():
    """Test if database can be initialized"""
    print("\nTesting database...")
    
    try:
        from app import create_app, db
        app = create_app()
        
        with app.app_context():
            # Try to create tables
            db.create_all()
            print("✅ Database tables created")
            return True
    except Exception as e:
        print(f"❌ Database test FAILED: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'app/__init__.py',
        'app/models/__init__.py',
        'app/models/user.py',
        'app/models/banner.py',
        'app/controllers/__init__.py',
        'app/controllers/auth_controller.py',
        'app/controllers/banner_controller.py',
        'app/services/__init__.py',
        'app/services/banner_service.py',
        'app/services/file_service.py',
        'app/utils/__init__.py',
        'app/utils/genbanner.py',
        'app/utils/openai_client.py',
        'app/config/__init__.py',
        'app/config/settings.py',
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files exist")
        return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("MVC STRUCTURE VERIFICATION TEST")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("App Creation", test_app_creation),
        ("Blueprints", test_blueprints),
        ("Routes", test_routes),
        ("Database", test_database),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! MVC structure is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
