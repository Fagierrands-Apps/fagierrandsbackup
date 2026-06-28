#!/usr/bin/env python3
"""
Live URL Diagnostic - Tests actual web server response and suggests fixes
Run from cPanel or local machine
"""

import sys
import os
import subprocess
import json

def run_command(cmd):
    """Execute shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def test_url(url):
    """Test URL with curl and analyze response"""
    print(f"🔍 Testing URL: {url}")
    print("="*60)
    
    # Test 1: HTTP Status
    print("\n[1] HTTP Status Check")
    code, stdout, stderr = run_command(f"curl -s -o /dev/null -w '%{{http_code}}' {url}")
    status = stdout.strip() if code == 0 else "ERROR"
    
    if status == "200":
        print(f"✅ Status: {status} OK")
    else:
        print(f"❌ Status: {status}")
        
    # Test 2: Response Headers
    print("\n[2] Response Headers")
    code, stdout, stderr = run_command(f"curl -I {url} 2>&1")
    if code == 0:
        for line in stdout.split('\n')[:10]:
            if line.strip():
                print(f"   {line}")
    
    # Test 3: Response Body
    print("\n[3] Response Body Sample")
    code, stdout, stderr = run_command(f"curl -s {url}")
    if code == 0:
        body = stdout[:500]
        print(body)
        
        # Analyze response
        if "404" in body or "Not Found" in body:
            return "404_ERROR"
        elif "500" in body or "Internal Server Error" in body:
            return "500_ERROR"
        elif "502" in body or "Bad Gateway" in body:
            return "502_ERROR"
        elif "<html" in body.lower() or "<!doctype" in body.lower():
            if "django" in body.lower() or "csrf" in body.lower():
                return "DJANGO_OK"
            else:
                return "HTML_NON_DJANGO"
        elif body.strip().startswith("{"):
            return "JSON_RESPONSE"
    
    return "UNKNOWN"

def diagnose_issue(result, server_path="/home3/distinc3/fagiserver.fagtone.com"):
    """Diagnose based on test result and suggest fixes"""
    print("\n" + "="*60)
    print("DIAGNOSIS & FIXES")
    print("="*60)
    
    if result == "404_ERROR":
        print("\n❌ ISSUE: 404 Not Found - Python app not loading")
        print("\nPOSSIBLE CAUSES:")
        print("1. passenger_wsgi.py has import error")
        print("2. Python App not started in cPanel")
        print("3. Application root path is wrong")
        print("4. Missing logs directory causing crash")
        
        print("\n🔧 FIXES TO TRY:")
        print("\n1. Check passenger_wsgi.py exists and imports work:")
        print(f"   cd {server_path}")
        print("   python3 passenger_wsgi.py")
        
        print("\n2. Check error logs:")
        print(f"   tail -50 {server_path}/../logs/*.error.log")
        print(f"   tail -50 {server_path}/logs/error.log")
        
        print("\n3. Verify logs directory exists:")
        print(f"   ls -la {server_path}/logs/")
        print(f"   mkdir -p {server_path}/logs")
        
        print("\n4. Restart Python App:")
        print("   cPanel → Setup Python App → Stop → Start → Restart")
        print(f"   touch {server_path}/tmp/restart.txt")
        
        print("\n5. Check Python App config:")
        print(f"   Application Root: {server_path}")
        print("   Application Startup File: passenger_wsgi.py")
        
    elif result == "500_ERROR":
        print("\n❌ ISSUE: 500 Internal Server Error - App crashed")
        print("\n🔧 CHECK:")
        print("1. Database connection")
        print("2. Environment variables (.env)")
        print("3. Error logs for Python traceback")
        
    elif result == "502_ERROR":
        print("\n❌ ISSUE: 502 Bad Gateway - App not responding")
        print("\n🔧 CHECK:")
        print("1. Python process running")
        print("2. Passenger configuration")
        print("3. Virtual environment activated")
        
    elif result == "DJANGO_OK":
        print("\n✅ SUCCESS: Django is responding!")
        
    else:
        print(f"\n⚠️  UNKNOWN RESPONSE: {result}")
        print("Review the response body above")

def main():
    url = "https://fagierrandsbackup.fagierrands.com/"
    
    print("🚀 Live URL Diagnostic Tool")
    print("="*60)
    
    # Run test
    result = test_url(url)
    
    # Diagnose
    diagnose_issue(result)
    
    print("\n" + "="*60)
    print("Diagnostic Complete")
    print("="*60)

if __name__ == "__main__":
    main()
