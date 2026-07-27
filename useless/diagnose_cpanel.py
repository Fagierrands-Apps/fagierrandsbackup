#!/usr/bin/env python3
"""
cPanel Deployment Diagnostic Script
Run this in cPanel Python App to diagnose 404 errors
Place this in ROOT: fagiserver.fagtone.com/diagnose_cpanel.py
"""

import os
import sys
from pathlib import Path

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def check_file_exists(filepath, description):
    exists = os.path.exists(filepath)
    status = "✅ FOUND" if exists else "❌ MISSING"
    print(f"{status}: {description}")
    print(f"   Path: {filepath}")
    if exists and os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        print(f"   Size: {size} bytes")
    return exists

def main():
    print("🔍 cPanel 404 Error Diagnostic")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    
    root_dir = os.getcwd()
    
    # Check passenger_wsgi.py in ROOT first
    print_section("PASSENGER_WSGI.PY CHECK (ROOT)")
    
    passenger_file = os.path.join(root_dir, "passenger_wsgi.py")
    if os.path.exists(passenger_file):
        print(f"✅ FOUND: {passenger_file}")
        with open(passenger_file, "r") as f:
            content = f.read()
            print("\nContent:")
            print(content)
            
            if "application" in content:
                print("\n✅ 'application' variable found")
            else:
                print("\n❌ MISSING 'application' variable - THIS CAUSES 404!")
                
            if "fagierrandsbackup.fagierrandsbackup.wsgi" in content:
                print("✅ Correct import path")
            else:
                print("❌ Wrong import path - should be 'fagierrandsbackup.fagierrandsbackup.wsgi'")
    else:
        print(f"❌ NOT FOUND: {passenger_file}")
        print("   THIS IS THE CAUSE OF 404 ERROR!")
        print("   passenger_wsgi.py MUST exist in application root")
    
    # Change to fagierrandsbackup directory
    app_dir = os.path.join(root_dir, "fagierrandsbackup")
    if os.path.exists(app_dir):
        os.chdir(app_dir)
        print(f"\n✅ Changed to: {os.getcwd()}")
    else:
        print(f"\n❌ ERROR: {app_dir} folder not found!")
        return
    
    # Check critical files
    print_section("CRITICAL FILES CHECK")
    
    files_to_check = [
        ("manage.py", "Django management script"),
        ("fagierrandsbackup/settings.py", "Django settings"),
        ("fagierrandsbackup/wsgi.py", "Django WSGI"),
        ("fagierrandsbackup/urls.py", "Django URL config"),
    ]
    
    all_exist = True
    for filepath, desc in files_to_check:
        if not check_file_exists(filepath, desc):
            all_exist = False
    
    # Check directories
    print_section("DIRECTORY STRUCTURE")
    
    dirs_to_check = [
        "accounts",
        "orders",
        "marketplace",
        "fagierrandsbackup",
        "logs",
        "templates",
    ]
    
    for dirname in dirs_to_check:
        exists = os.path.isdir(dirname)
        status = "✅" if exists else "❌"
        print(f"{status} {dirname}/")
    
    # Try importing Django
    print_section("DJANGO IMPORT TEST")
    
    try:
        sys.path.insert(0, os.getcwd())
        import django
        print(f"✅ Django imported successfully (version {django.VERSION})")
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fagierrandsbackup.settings')
        django.setup()
        print("✅ Django setup successful")
        
        from django.conf import settings
        print(f"✅ Settings loaded")
        print(f"   DEBUG = {settings.DEBUG}")
        print(f"   ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
        
    except Exception as e:
        print(f"❌ Django import/setup failed:")
        print(f"   Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Final diagnosis
    print_section("DIAGNOSIS - 404 ERROR ROOT CAUSE")
    
    passenger_exists = os.path.exists(os.path.join(root_dir, "passenger_wsgi.py"))
    
    if not passenger_exists:
        print("❌ ROOT CAUSE: passenger_wsgi.py MISSING in root folder!")
        print(f"   Expected location: {root_dir}/passenger_wsgi.py")
        print("\n   SOLUTION:")
        print("   1. Create passenger_wsgi.py in root folder")
        print("   2. Add Django WSGI import")
        print("   3. Restart Python App")
    elif not all_exist:
        print("❌ Django files missing in fagierrandsbackup/")
        print("   Solution: Re-upload deployment files")
    else:
        print("✅ All files present!")
        print("   If still 404:")
        print("   1. Check passenger_wsgi.py content above")
        print("   2. Verify 'application' variable exists")
        print("   3. Restart Python App in cPanel")
    
    print("\n" + "="*60)
    print("Diagnostic complete!")
    print("="*60)

if __name__ == "__main__":
    main()
