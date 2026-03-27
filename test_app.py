"""
Test script for Asset Manager application.
Verifies that all components work correctly.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import PyQt5
        print("  ✓ PyQt5 imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import PyQt5: {e}")
        return False
    
    try:
        import sqlite3
        print("  ✓ sqlite3 imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import sqlite3: {e}")
        return False
    
    return True

def test_database():
    """Test database operations."""
    print("\nTesting database...")
    try:
        from database import AssetDatabase
        
        # Create test database
        db = AssetDatabase("test_assets.db")
        
        # Add test asset
        asset_id = db.add_asset(
            name="Test Laptop",
            category="Electronics",
            description="Test description",
            location="Office",
            purchase_price=1000.00,
            current_value=800.00,
            purchase_date="2024-01-01",
            condition="Good",
            notes="Test notes"
        )
        print(f"  ✓ Added test asset with ID: {asset_id}")
        
        # Retrieve asset
        asset = db.get_asset_by_id(asset_id)
        if asset and asset['name'] == "Test Laptop":
            print("  ✓ Retrieved asset successfully")
        else:
            print("  ✗ Failed to retrieve asset")
            return False
        
        # Update asset
        db.update_asset(
            asset_id=asset_id,
            name="Updated Laptop",
            category="Electronics",
            description="Updated description",
            location="Home",
            purchase_price=1000.00,
            current_value=750.00,
            purchase_date="2024-01-01",
            condition="Good",
            notes="Updated notes"
        )
        print("  ✓ Updated asset successfully")
        
        # Get all assets
        assets = db.get_all_assets()
        print(f"  ✓ Retrieved {len(assets)} assets")
        
        # Get totals
        total_purchase = db.get_total_purchase_value()
        total_current = db.get_total_current_value()
        print(f"  ✓ Total purchase value: ${total_purchase:,.2f}")
        print(f"  ✓ Total current value: ${total_current:,.2f}")
        
        # Delete asset
        db.delete_asset(asset_id)
        print("  ✓ Deleted asset successfully")
        
        # Clean up
        db.close()
        if os.path.exists("test_assets.db"):
            os.remove("test_assets.db")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Database test failed: {e}")
        return False

def test_ui_import():
    """Test that UI module can be imported."""
    print("\nTesting UI module...")
    try:
        from ui import AssetManagerUI, AssetDialog
        print("  ✓ UI modules imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed to import UI modules: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("Asset Manager - Component Tests")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test database
    if not test_database():
        all_passed = False
    
    # Test UI import
    if not test_ui_import():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("All tests passed! ✓")
        print("\nYou can now run the application:")
        print("  python main.py")
        print("\nOr build the executable:")
        print("  build_all.bat")
    else:
        print("Some tests failed! ✗")
        print("\nPlease check the errors above and fix them.")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
