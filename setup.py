"""
Setup and Installation Script for VJudge Crawler
Run this script to verify everything is set up correctly
"""

import subprocess
import sys
import os


def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.7+)")
        return False


def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    requirements = [
        "requests",
        "beautifulsoup4", 
        "selenium",
        "pandas",
        "webdriver-manager"
    ]
    
    try:
        for package in requirements:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("✓ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install packages: {e}")
        return False


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    test_modules = [
        ("requests", "requests"),
        ("beautifulsoup4", "bs4"),
        ("selenium", "selenium"),
        ("pandas", "pandas"),
        ("webdriver_manager", "webdriver_manager")
    ]
    
    for package, module in test_modules:
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (failed to import)")
            return False
    
    return True


def test_crawler():
    """Test basic crawler functionality"""
    print("Testing crawler initialization...")
    
    try:
        from vjudge_crawler import VJudgeRankingCrawler
        
        # Test initialization
        crawler = VJudgeRankingCrawler(headless=True)
        print("✓ Crawler initialized successfully")
        
        # Close crawler
        crawler.close()
        print("✓ Crawler closed successfully")
        
        return True
    except Exception as e:
        print(f"✗ Crawler test failed: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    
    directories = ["output", "examples"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory exists: {directory}")
    
    return True


def show_usage_examples():
    """Show usage examples"""
    print("\n" + "=" * 50)
    print("SETUP COMPLETE! 🎉")
    print("=" * 50)
    print("\nHow to use the VJudge Crawler:")
    print()
    print("1. GUI Interface (Recommended):")
    print("   python vjudge_gui.py")
    print()
    print("2. Command Line:")
    print("   python crawl_cli.py 739901")
    print("   python crawl_cli.py 739901 739902 --headless")
    print()
    print("3. Run Examples:")
    print("   python examples.py")
    print()
    print("4. Test Installation:")
    print("   python test_crawler.py")
    print()
    print("Files and Directories:")
    print("- vjudge_crawler.py   : Main crawler module")
    print("- vjudge_gui.py       : GUI application")
    print("- crawl_cli.py        : Command-line interface")
    print("- examples.py         : Usage examples")
    print("- test_crawler.py     : Test functionality")
    print("- output/             : CSV files will be saved here")
    print("- README.md           : Detailed documentation")
    print()
    print("For more information, see README.md")


def main():
    """Main setup function"""
    print("VJudge Crawler Setup")
    print("=" * 30)
    print()
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    print()
    
    # Install requirements
    if success and not install_requirements():
        success = False
    print()
    
    # Test imports
    if success and not test_imports():
        success = False
    print()
    
    # Test crawler
    if success and not test_crawler():
        success = False
    print()
    
    # Create directories
    if success and not create_directories():
        success = False
    print()
    
    if success:
        show_usage_examples()
    else:
        print("❌ Setup failed!")
        print("Please fix the errors above and run this script again.")
        print()
        print("Common solutions:")
        print("- Make sure you have Python 3.7+ installed")
        print("- Make sure you have Chrome browser installed") 
        print("- Try running: pip install --upgrade pip")
        print("- Check your internet connection")


if __name__ == "__main__":
    main()
