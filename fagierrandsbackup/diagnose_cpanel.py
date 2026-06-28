#!/usr/bin/env python3
"""
cPanel Deployment Diagnostic Script
Run this in cPanel Python App to diagnose 404 errors
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
    print("🔍 cPanel Deployment Diagnostic")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    
    # Check critical files
    print_section("CRITICAL FILES CHECK")
    
    files_to_check = [
        ("passenger_wsgi.py", "Passenger WSGI entry point"),
        ("manage.py", "Django management script"),
        ("requirements.txt", "Dependencies file"),
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
        "venv",
        "logs",
        "tmp",
        "static",
    ]
    
    for dirname in dirs_to_check:
        exists = os.path.isdir(dirname)
        status = "✅" if exists else "❌"
        print(f"{status} {dirname}/")
    
    # Check passenger_wsgi.py content
    print_section("PASSENGER_WSGI.PY CONTENT")
    
    if os.path.exists("passenger_wsgi.py"):
        with open("passenger_wsgi.py", "r") as f:
            content = f.read()
            print(content)
            
            # Check for common issues
            if "application" in content:
                print("\n✅ 'application' variable found")
            else:
                print("\n❌ 'application' variable NOT found")
    
    # Check environment variables
    print_section("ENVIRONMENT VARIABLES")
    
    env_vars = [
        "DEBUG",
        "SECRET_KEY",
        "PG_DB_NAME",
        "PG_USER",
        "PG_HOST",
        "ALLOWED_HOSTS",
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive data
            if var in ["SECRET_KEY", "PG_PASSWORD"]:
                display = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
            else:
                display = value
            print(f"✅ {var} = {display}")
        else:
            print(f"❌ {var} = NOT SET")
    
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
    
    # Check permissions
    print_section("FILE PERMISSIONS")
    
    files_perms = [
        "passenger_wsgi.py",
        "manage.py",
    ]
    
    for filepath in files_perms:
        if os.path.exists(filepath):
            perms = oct(os.stat(filepath).st_mode)[-3:]
            print(f"{filepath}: {perms}")
    
    # List all files in current directory
    print_section("CURRENT DIRECTORY CONTENTS")
    
    items = sorted(os.listdir("."))[:20]  # First 20 items
    for item in items:
        item_type = "DIR" if os.path.isdir(item) else "FILE"
        print(f"  [{item_type}] {item}")
    
    # Final diagnosis
    print_section("DIAGNOSIS")
    
    if not all_exist:
        print("❌ CRITICAL FILES MISSING!")
        print("   Solution: Re-upload and extract the deployment zip")
    elif not os.path.exists("venv"):
        print("❌ VIRTUAL ENVIRONMENT MISSING!")
        print("   Solution: Run 'python3 -m venv venv' in cPanel Console")
    elif not os.environ.get("PG_DB_NAME"):
        print("❌ ENVIRONMENT VARIABLES NOT SET!")
        print("   Solution: Set variables in cPanel Python App settings")
    else:
        print("✅ All checks passed!")
        print("   If still getting 404, check:")
        print("   1. Python App is pointing to correct directory")
        print("   2. Application startup file is set to 'passenger_wsgi.py'")
        print("   3. Restart the app via cPanel")
    
    print("\n" + "="*60)
    print("Diagnostic complete!")
    print("="*60)

if __name__ == "__main__":
    main()
