#!/usr/bin/env python3
"""
Development runner script for Notify Rohan
Provides easy commands for development, testing, and building
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'kivy',
        'kivymd', 
        'pillow',
        'python-dateutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing dependencies:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False  # Added return value for clarity
    print("✅ All dependencies are installed")
    return True

def clean_build():
    """Clean build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    directories_to_clean = [
        ".buildozer",
        "bin", 
        "__pycache__",
        ".pytest_cache",
        "build",
        "dist"
    ]
    
    files_to_clean = [
        "*.pyc",
        "*.pyo",
        "*.egg-info"
    ]
    
    import shutil
    import glob
    
    for directory in directories_to_clean:
        if Path(directory).exists():
            shutil.rmtree(directory)
            print(f"  Removed: {directory}")
    
    for pattern in files_to_clean:
        for file_path in glob.glob(pattern, recursive=True):
            os.remove(file_path)
            print(f"  Removed: {file_path}")
    
    print("✅ Cleanup complete")
    return True

def setup_dev():
    """Setup development environment"""
    print("⚙️  Setting up development environment...")
    
    # Install dependencies
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    
    # Create assets
    if not create_assets():
        print("⚠️  Failed to create assets, but continuing...")
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    print("✅ Data directory created")
    
    # Create sample data if it doesn't exist
    try:
        from utils import NotificationManager, ThemeManager
        
        # Initialize managers to create default files
        nm = NotificationManager()
        nm.load_notifications()
        
        tm = ThemeManager()
        tm.load_settings()
        
        print("✅ Sample data created")
    except Exception as e:
        print(f"⚠️  Error creating sample data: {e}")
    
    print("✅ Development environment setup complete!")
    print("\nNext steps:")
    print("  python run.py app      # Run the application")
    print("  python run.py test     # Run tests") 
    print("  python run.py android  # Build for Android")
    
    return True

def show_info():
    """Show project information"""
    print("📋 Notify Rohan - Project Information")
    print("=" * 40)
    
    # Python version
    print(f"Python: {sys.version.split()[0]}")
    
    # Check dependencies
    dependencies = {
        'kivy': 'Kivy GUI Framework',
        'kivymd': 'Material Design Components', 
        'pillow': 'Image Processing',
        'python-dateutil': 'Date/Time Utilities'
    }
    
    print("\nDependencies:")
    for package, description in dependencies.items():
        try:
            module = __import__(package.replace('-', '_'))
            version = getattr(module, '__version__', 'Unknown')
            status = "✅"
        except ImportError:
            version = "Not installed"
            status = "❌"
        
        print(f"  {status} {package}: {version} - {description}")
    
    # Project structure
    print(f"\nProject Structure:")
    important_files = [
        "main.py",
        "screens.py", 
        "utils.py",
        "assets.py",
        "requirements.txt",
        "buildozer.spec"
    ]
    
    for file in important_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"  ✅ {file} ({size} bytes)")
        else:
            print(f"  ❌ {file} (missing)")
    
    # Data files
    print(f"\nData Files:")
    data_files = ["data/notifications.json", "data/settings.json"]
    for file in data_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} (will be created on first run)")

def create_buildozer_spec():
    """Create a basic buildozer.spec file"""
    print("📱 Creating buildozer.spec file...")
    
    spec_content = """[app]
title = Notify Rohan
package.name = notifyrohan
package.domain = com.rohan.notifyrohan

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0
requirements = python3,kivy,kivymd,pillow,python-dateutil

[buildozer]
log_level = 2

[app]
presplash.filename = assets/presplash.png
icon.filename = assets/icon.png

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
warn_on_root = 1
"""
    
    try:
        with open('buildozer.spec', 'w') as f:
            f.write(spec_content)
        print("✅ buildozer.spec created")
        return True
    except Exception as e:
        print(f"❌ Error creating buildozer.spec: {e}")
        return False

def run_app():
    """Run the main application"""
    print("🚀 Starting Notify Rohan...")
    
    if not check_dependencies():
        return False
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Run the app
    try:
        from main import NotifyRohanApp
        app = NotifyRohanApp()
        app.run()
        return True
    except Exception as e:
        print(f"❌ Error running app: {e}")
        return False

def create_assets():
    """Generate application assets"""
    print("🎨 Creating application assets...")
    
    try:
        # Check if PIL is available
        import PIL
        
        # Run asset creation script
        exec(open('assets.py').read())
        return True
    except ImportError:
        print("❌ Pillow (PIL) is required to generate assets")
        print("Install with: pip install pillow")
        return False
    except FileNotFoundError:
        print("❌ assets.py file not found")
        return False
    except Exception as e:
        print(f"❌ Error creating assets: {e}")
        return False

def run_tests():
    """Run application tests"""
    print("🧪 Running tests...")
    
    test_files = list(Path(".").glob("test_*.py")) + list(Path("tests").glob("*.py"))
    
    if not test_files:
        print("⚠️  No test files found")
        return True
    
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "-v"], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ pytest not found. Install with: pip install pytest")
        return False

def build_android():
    """Build Android APK using Buildozer"""
    print("📱 Building Android APK...")
    
    if not Path("buildozer.spec").exists():
        print("❌ buildozer.spec not found")
        return False
    
    try:
        # Check if buildozer is installed
        subprocess.run(["buildozer", "--version"], check=True, 
                      capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ Buildozer not found. Install with: pip install buildozer")
        return False
    
    try:
        print("This may take a while...")
        result = subprocess.run(["buildozer", "android", "debug"], 
                              capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error building Android APK: {e}")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Notify Rohan Development Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available commands:
  app       Run the application
  assets    Generate application assets (icons, images)
  test      Run tests
  android   Build Android APK (requires buildozer)
  clean     Clean build artifacts
  setup     Setup development environment
  info      Show project information
  spec      Create buildozer.spec file
  
Examples:
  python run.py app
  python run.py setup
  python run.py android
        """
    )
    
    parser.add_argument(
        'command',
        choices=['app', 'assets', 'test', 'android', 'clean', 'setup', 'info', 'spec'],
        help='Command to run'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    # Command dispatch
    commands = {
        'app': run_app,
        'assets': create_assets,
        'test': run_tests,
        'android': build_android,
        'clean': clean_build,
        'setup': setup_dev,
        'info': show_info,
        'spec': create_buildozer_spec
    }
    
    command_func = commands.get(args.command)
    if command_func:
        success = command_func()
        if not success:
            sys.exit(1)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'kivy',
        'kivymd', 
        'pillow',
        'python-dateutil'
    ]
    
    import_map = {
        'kivy': 'kivy',
        'kivymd': 'kivymd',
        'pillow': 'PIL',
        'python-dateutil': 'dateutil'
    }
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(import_map[package])
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing dependencies:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    print("✅ All dependencies are installed")
    return True

if __name__ == "__main__":
    main()