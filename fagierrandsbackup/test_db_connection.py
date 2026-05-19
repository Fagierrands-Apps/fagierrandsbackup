#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Load environment
from dotenv import load_dotenv
load_dotenv(BASE_DIR / '.env')

print("=" * 60)
print("DATABASE CONFIGURATION CHECK")
print("=" * 60)

# Check what's in environment
print("\n1. Environment Variables:")
print(f"   PG_DB_NAME: {os.getenv('PG_DB_NAME', 'NOT SET')}")
print(f"   PG_USER: {os.getenv('PG_USER', 'NOT SET')}")
print(f"   PG_PASSWORD: {'***' if os.getenv('PG_PASSWORD') else 'NOT SET'}")
print(f"   PG_HOST: {os.getenv('PG_HOST', 'NOT SET')}")
print(f"   PG_PORT: {os.getenv('PG_PORT', 'NOT SET')}")
print(f"   DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')}")

# Load Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fagierrandsbackup.settings')
import django
django.setup()

from django.conf import settings

print("\n2. Django Database Settings:")
db_config = settings.DATABASES['default']
print(f"   ENGINE: {db_config.get('ENGINE')}")
print(f"   NAME: {db_config.get('NAME')}")
print(f"   USER: {db_config.get('USER')}")
print(f"   HOST: {db_config.get('HOST')}")
print(f"   PORT: {db_config.get('PORT')}")

# Test connection
print("\n3. Testing Database Connection...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database(), current_user;")
        db_name, db_user = cursor.fetchone()
        print(f"   ✓ Connected to database: {db_name}")
        print(f"   ✓ Connected as user: {db_user}")
        print(f"   ✓ Connection successful!")
except Exception as e:
    print(f"   ✗ Connection failed: {e}")

print("=" * 60)
