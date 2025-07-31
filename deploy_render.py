#!/usr/bin/env python3
"""
Deployment Helper Script for Remindly Flask API
Validates configuration and provides deployment guidance
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(filename):
    """Check if a required file exists"""
    if Path(filename).exists():
        print(f"✅ {filename}")
        return True
    else:
        print(f"❌ {filename} - MISSING!")
        return False

def check_requirements():
    """Check if all required files are present"""
    print("🔍 Checking deployment requirements...")
    print("=" * 50)
    
    required_files = [
        'app.py',
        'requirements.txt', 
        'Procfile',
        'runtime.txt',
        'config.py'
    ]
    
    all_good = True
    for file in required_files:
        if not check_file_exists(file):
            all_good = False
    
    print("=" * 50)
    return all_good

def check_environment_variables():
    """Check if environment variables are set"""
    print("\n🔐 Checking environment variables...")
    print("=" * 50)
    
    required_vars = ['JWT_SECRET_KEY', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} - SET")
        else:
            print(f"❌ {var} - NOT SET")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Make sure to set these in your hosting platform!")
    
    print("=" * 50)
    return len(missing_vars) == 0

def show_deployment_urls():
    """Show potential deployment URLs"""
    print("\n🌐 Potential Deployment URLs:")
    print("=" * 50)
    
    app_names = ['remindly-api', 'remindly', 'task-manager-api']
    
    print("Render (Recommended):")
    for name in app_names:
        print(f"  https://{name}.onrender.com")
    
    print("\nRailway:")
    for name in app_names:
        print(f"  https://{name}.railway.app")
    
    print("\nVercel:")
    for name in app_names:
        print(f"  https://{name}.vercel.app")
    
    print("=" * 50)

def show_test_commands():
    """Show test commands for the deployed API"""
    print("\n🧪 Test Commands for Deployed API:")
    print("=" * 50)
    
    print("Replace 'YOUR_URL' with your actual deployment URL")
    print()
    
    commands = [
        ("Health Check", "curl https://YOUR_URL/"),
        ("API Status", "curl https://YOUR_URL/api/"),
        ("Register User", """curl -X POST https://YOUR_URL/api/register \\
  -H "Content-Type: application/json" \\
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'"""),
        ("Login", """curl -X POST https://YOUR_URL/api/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "testuser", "password": "password123"}'""")
    ]
    
    for name, cmd in commands:
        print(f"{name}:")
        print(f"  {cmd}")
        print()

def main():
    """Main deployment helper function"""
    print("🚀 Remindly Flask API Deployment Helper")
    print("=" * 60)
    
    # Check requirements
    files_ok = check_requirements()
    
    # Check environment variables
    env_ok = check_environment_variables()
    
    # Show deployment URLs
    show_deployment_urls()
    
    # Show test commands
    show_test_commands()
    
    # Summary
    print("\n📋 Deployment Summary:")
    print("=" * 50)
    
    if files_ok and env_ok:
        print("✅ All requirements met! Ready to deploy.")
        print("\n🎯 Next Steps:")
        print("1. Push your code to GitHub")
        print("2. Go to render.com and create a new Web Service")
        print("3. Connect your GitHub repository")
        print("4. Set environment variables in Render dashboard")
        print("5. Deploy!")
    else:
        print("❌ Some requirements are missing.")
        if not files_ok:
            print("   - Fix missing files")
        if not env_ok:
            print("   - Set environment variables in hosting platform")
    
    print("\n📖 For detailed instructions, see: DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main() 