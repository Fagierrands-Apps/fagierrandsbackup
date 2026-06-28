#!/usr/bin/env python3
"""
Apply security settings to production settings.py
Run this in cPanel to update the deployed settings.py
"""

import os
import shutil
from datetime import datetime

def apply_security_settings():
    settings_path = "fagierrandsbackup/fagierrandsbackup/settings.py"
    
    if not os.path.exists(settings_path):
        print(f"❌ ERROR: {settings_path} not found!")
        print("   Make sure you're running this from the app root directory.")
        return False
    
    # Backup first
    backup_path = f"{settings_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(settings_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    
    # Read current settings
    with open(settings_path, 'r') as f:
        content = f.read()
    
    # Check if already applied
    if "SESSION_COOKIE_SECURE = True" in content:
        print("✅ Security settings already applied!")
        return True
    
    # Find insertion point (after CSRF_TRUSTED_ORIGINS)
    if "CSRF_TRUSTED_ORIGINS = [" not in content:
        print("❌ ERROR: Could not find CSRF_TRUSTED_ORIGINS in settings.py")
        return False
    
    security_block = '''

# ============================================
# PRODUCTION SECURITY SETTINGS
# ============================================

# Force HTTPS for all requests
SECURE_SSL_REDIRECT = not DEBUG

# Secure cookie settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Additional security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
'''
    
    # Find the end of CSRF_TRUSTED_ORIGINS block
    lines = content.split('\n')
    insert_index = -1
    in_csrf_block = False
    
    for i, line in enumerate(lines):
        if 'CSRF_TRUSTED_ORIGINS' in line:
            in_csrf_block = True
        elif in_csrf_block and line.strip() == ']':
            insert_index = i + 1
            break
    
    if insert_index == -1:
        print("❌ ERROR: Could not find insertion point")
        return False
    
    # Insert security settings
    lines.insert(insert_index, security_block)
    
    # Write updated content
    with open(settings_path, 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Security settings applied successfully!")
    print("\nAdded settings:")
    print("  • SESSION_COOKIE_SECURE = True")
    print("  • CSRF_COOKIE_SECURE = True")
    print("  • SECURE_SSL_REDIRECT = True (when DEBUG=False)")
    print("  • SECURE_HSTS_SECONDS = 31536000")
    print("  • And more...")
    
    print("\n⚠️  NEXT STEPS:")
    print("  1. Upload updated settings.py to cPanel")
    print("  2. Restart Python App")
    print("  3. Test the site")
    
    return True

if __name__ == "__main__":
    print("🔒 Applying Security Settings")
    print("="*60)
    apply_security_settings()
    print("="*60)
