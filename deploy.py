#!/usr/bin/env python3
"""
Deployment Helper Script
Generates secure keys and prepares the application for deployment.
"""

import secrets
import string
import os

def generate_secret_key(length=32):
    """Generate a secure random secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    print("🔧 Flask API Deployment Helper")
    print("=" * 40)
    
    # Generate secure keys
    jwt_secret = generate_secret_key(64)
    flask_secret = generate_secret_key(32)
    
    print("\n✅ Generated secure keys:")
    print(f"JWT_SECRET_KEY: {jwt_secret}")
    print(f"SECRET_KEY: {flask_secret}")
    
    print("\n📋 Environment Variables for Render:")
    print("=" * 40)
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print(f"SECRET_KEY={flask_secret}")
    print("FLASK_ENV=production")
    
    print("\n🚀 Deployment Steps:")
    print("1. Go to https://render.com")
    print("2. Sign up with GitHub")
    print("3. Click 'New +' → 'Web Service'")
    print("4. Connect your repository")
    print("5. Configure:")
    print("   - Name: remindly")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: gunicorn app:app")
    print("6. Add the environment variables above")
    print("7. Deploy!")
    
    print(f"\n🌐 Your API will be available at: https://remindly.onrender.com")
    
    # Save keys to a file (for reference only)
    with open('deployment_keys.txt', 'w') as f:
        f.write(f"JWT_SECRET_KEY={jwt_secret}\n")
        f.write(f"SECRET_KEY={flask_secret}\n")
        f.write("FLASK_ENV=production\n")
    
    print("\n💾 Keys saved to 'deployment_keys.txt' (keep this secure!)")
    print("⚠️  Remember to add deployment_keys.txt to .gitignore")

if __name__ == "__main__":
    main() 