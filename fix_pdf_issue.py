#!/usr/bin/env python3
"""
GPT-Researcher PDF Issue Fix Script

This script helps fix the WeasyPrint PDF generation issue on macOS by:
1. Checking if WeasyPrint can be imported
2. Providing installation instructions for system dependencies
3. Configuring the environment to disable PDF generation if needed
"""

import os
import sys
import subprocess
from pathlib import Path


def check_weasyprint():
    """Check if WeasyPrint can be imported successfully."""
    try:
        import weasyprint
        print("✅ WeasyPrint is working correctly!")
        return True
    except ImportError as e:
        print(f"❌ WeasyPrint import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ WeasyPrint has dependency issues: {e}")
        return False


def check_homebrew():
    """Check if Homebrew is installed."""
    try:
        result = subprocess.run(['which', 'brew'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Homebrew is installed")
            return True
        else:
            print("❌ Homebrew is not installed")
            return False
    except Exception:
        print("❌ Could not check Homebrew installation")
        return False


def install_dependencies():
    """Install WeasyPrint dependencies using Homebrew."""
    if not check_homebrew():
        print("\n📋 Please install Homebrew first:")
        print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        return False
    
    print("\n🔧 Installing WeasyPrint dependencies...")
    try:
        subprocess.run(['brew', 'install', 'pango', 'gdk-pixbuf', 'libffi'], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def configure_env_file():
    """Configure the .env file to disable PDF generation."""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    # Create .env from .env.example if it doesn't exist
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from .env.example...")
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
    
    # Read current .env content
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Check if ENABLE_PDF_GENERATION is already set
        if 'ENABLE_PDF_GENERATION' in content:
            # Update existing setting
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('ENABLE_PDF_GENERATION'):
                    lines[i] = 'ENABLE_PDF_GENERATION=false'
                    break
            content = '\n'.join(lines)
        else:
            # Add new setting
            content += '\n# PDF Generation disabled due to WeasyPrint issues\nENABLE_PDF_GENERATION=false\n'
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Updated .env file to disable PDF generation")
        return True
    else:
        print("❌ Could not find or create .env file")
        return False


def main():
    """Main function to run the fix script."""
    print("🔍 GPT-Researcher PDF Issue Fix Script")
    print("=" * 50)
    
    # Check current WeasyPrint status
    print("\n1. Checking WeasyPrint status...")
    weasyprint_works = check_weasyprint()
    
    if weasyprint_works:
        print("\n🎉 No issues found! PDF generation should work correctly.")
        return
    
    print("\n2. WeasyPrint has issues. Checking system dependencies...")
    
    # Try to install dependencies
    print("\n3. Attempting to install system dependencies...")
    deps_installed = install_dependencies()
    
    if deps_installed:
        print("\n4. Testing WeasyPrint again...")
        if check_weasyprint():
            print("\n🎉 Fixed! PDF generation should now work correctly.")
            return
    
    # If still not working, disable PDF generation
    print("\n5. WeasyPrint still has issues. Disabling PDF generation...")
    if configure_env_file():
        print("\n✅ Configuration updated!")
        print("\n📋 Summary:")
        print("   - PDF generation has been disabled")
        print("   - Reports will be generated in Markdown and DOCX formats instead")
        print("   - You can still manually convert Markdown files to PDF using other tools")
        print("\n💡 To re-enable PDF generation later, set ENABLE_PDF_GENERATION=true in your .env file")
    else:
        print("\n❌ Could not update configuration. Please manually add this line to your .env file:")
        print("   ENABLE_PDF_GENERATION=false")


if __name__ == "__main__":
    main()
