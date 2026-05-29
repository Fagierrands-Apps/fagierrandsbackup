#!/usr/bin/env python3
"""
Quick verification script to check if fixes are working
"""
import os
import sys

print("=" * 60)
print("SERVER FIX VERIFICATION")
print("=" * 60)

# Check 1: Verify passenger_wsgi.py has OpenBLAS fix
print("\n1. Checking passenger_wsgi.py...")
try:
    with open('passenger_wsgi.py', 'r') as f:
        content = f.read()
        if "OPENBLAS_NUM_THREADS" in content:
            print("   ✅ OpenBLAS thread limit configured")
        else:
            print("   ❌ OpenBLAS thread limit NOT found")
except Exception as e:
    print(f"   ❌ Error reading file: {e}")

# Check 2: Verify export_views.py has lazy import
print("\n2. Checking orders/export_views.py...")
try:
    with open('fagierrandsbackup/orders/export_views.py', 'r') as f:
        content = f.read()
        lines = content.split('\n')
        
        # Check if openpyxl is NOT imported at module level (first 15 lines)
        module_level = '\n'.join(lines[:15])
        if 'from openpyxl import' not in module_level:
            print("   ✅ openpyxl import moved to method level")
        else:
            print("   ❌ openpyxl still imported at module level")
            
        # Check if it's imported inside the method
        if 'def get(self, request' in content and 'from openpyxl import' in content:
            print("   ✅ openpyxl imported inside method")
        else:
            print("   ⚠️  Could not verify method-level import")
except Exception as e:
    print(f"   ❌ Error reading file: {e}")

# Check 3: Verify restart file exists
print("\n3. Checking restart file...")
if os.path.exists('tmp/restart.txt'):
    print("   ✅ Restart file created")
    import time
    mtime = os.path.getmtime('tmp/restart.txt')
    print(f"   📅 Last modified: {time.ctime(mtime)}")
else:
    print("   ❌ Restart file NOT found")

print("\n" + "=" * 60)
print("NEXT STEPS:")
print("=" * 60)
print("1. Wait 10-30 seconds for server to restart")
print("2. Check stderr.log for errors:")
print("   tail -f stderr.log")
print("3. Test base URL:")
print("   curl https://fagiserver.fagtone.com/")
print("4. Check for OpenBLAS errors in logs")
print("=" * 60)
