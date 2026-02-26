"""
Quick test to verify RPIN backend setup
Run this after setup to ensure everything is configured correctly
"""
import sys
from pathlib import Path

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing package imports...")
    
    packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "pandas",
        "numpy",
        "sklearn",
        "xgboost",
        "requests",
        "sqlalchemy"
    ]
    
    failed = []
    for package in packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package}")
            failed.append(package)
    
    if failed:
        print(f"\n❌ Failed to import: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All packages imported successfully!")
    return True


def test_directory_structure():
    """Test that all required directories exist"""
    print("\nTesting directory structure...")
    
    required_dirs = [
        "app",
        "app/core",
        "app/api",
        "app/api/v1",
        "app/models",
        "app/services",
        "app/ml",
        "app/data",
        "data"
    ]
    
    missing = []
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/")
            missing.append(dir_path)
    
    if missing:
        print(f"\n❌ Missing directories: {', '.join(missing)}")
        return False
    
    print("\n✅ All directories exist!")
    return True


def test_data_files():
    """Test that data files exist"""
    print("\nTesting data files...")
    
    data_files = [
        "data/crops.json",
        "data/markets.json",
        "data/distances.json"
    ]
    
    missing = []
    for file_path in data_files:
        path = Path(file_path)
        if path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path}")
            missing.append(file_path)
    
    if missing:
        print(f"\n❌ Missing data files: {', '.join(missing)}")
        return False
    
    print("\n✅ All data files exist!")
    return True


def test_config():
    """Test that configuration loads correctly"""
    print("\nTesting configuration...")
    
    try:
        from app.core.config import settings
        print(f"  ✓ Project: {settings.PROJECT_NAME}")
        print(f"  ✓ Version: {settings.VERSION}")
        print(f"  ✓ API Prefix: {settings.API_V1_PREFIX}")
        print("\n✅ Configuration loaded successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Configuration error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("RPIN Backend Setup Verification")
    print("=" * 60)
    print()
    
    tests = [
        test_imports,
        test_directory_structure,
        test_data_files,
        test_config
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 60)
    if all(results):
        print("🎉 All tests passed! Setup is complete.")
        print("\nYou can now run the server:")
        print("  python main.py")
        print("\nOr:")
        print("  uvicorn main:app --reload")
        print("\nAPI docs will be available at:")
        print("  http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
