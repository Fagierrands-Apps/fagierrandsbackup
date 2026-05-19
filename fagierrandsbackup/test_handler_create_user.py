#!/usr/bin/env python
"""
Test script for handler create user endpoint
"""
import os
import django
import sys

# Setup Django
sys.path.insert(0, '/home/fagitone/Desktop/xxx/fagierrandsbackup27/fagierrandsbackup')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fagierrandsbackup.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

def test_handler_create_user():
    print("=" * 60)
    print("Testing Handler Create User Endpoint")
    print("=" * 60)
    
    # Create or get a handler user for testing
    handler, created = User.objects.get_or_create(
        username='test_handler',
        defaults={
            'phone_number': '+254700000000',
            'email': 'handler@test.com',
            'first_name': 'Test',
            'last_name': 'Handler',
            'user_type': 'handler',
            'is_verified': True
        }
    )
    if created:
        handler.set_password('testpass123')
        handler.save()
        print(f"✓ Created test handler: {handler.username}")
    else:
        print(f"✓ Using existing handler: {handler.username}")
    
    # Create API client
    client = APIClient()
    
    # Login as handler
    login_response = client.post('/accounts/login/', {
        'username': 'test_handler',
        'password': 'testpass123'
    })
    
    if login_response.status_code == 200:
        token = login_response.data.get('access')
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        print(f"✓ Handler logged in successfully")
    else:
        print(f"✗ Login failed: {login_response.data}")
        return
    
    # Test 1: Create a client user
    print("\n--- Test 1: Create Client User ---")
    client_data = {
        'phone_number': '+254711111111',
        'email': 'testclient@example.com',
        'first_name': 'Test',
        'last_name': 'Client',
        'user_type': 'client',
        'password': 'clientpass123'
    }
    
    response = client.post('/accounts/handler/create-user/', client_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    
    if response.status_code == 201:
        print("✓ Client user created successfully")
        # Verify user exists
        user = User.objects.get(phone_number='+254711111111')
        print(f"  - User ID: {user.id}")
        print(f"  - Username: {user.username}")
        print(f"  - User Type: {user.user_type}")
        print(f"  - Account Manager: {user.account_manager}")
    else:
        print(f"✗ Failed to create client user")
    
    # Test 2: Create an assistant user
    print("\n--- Test 2: Create Assistant User ---")
    assistant_data = {
        'phone_number': '+254722222222',
        'email': 'testassistant@example.com',
        'first_name': 'Test',
        'last_name': 'Assistant',
        'user_type': 'assistant',
        'password': 'assistantpass123'
    }
    
    response = client.post('/accounts/handler/create-user/', assistant_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    
    if response.status_code == 201:
        print("✓ Assistant user created successfully")
    else:
        print(f"✗ Failed to create assistant user")
    
    # Test 3: Try to create duplicate user
    print("\n--- Test 3: Duplicate Phone Number (Should Fail) ---")
    response = client.post('/accounts/handler/create-user/', client_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    
    if response.status_code == 409:
        print("✓ Correctly rejected duplicate phone number")
    else:
        print(f"✗ Should have rejected duplicate")
    
    # Test 4: Missing required fields
    print("\n--- Test 4: Missing Required Fields (Should Fail) ---")
    incomplete_data = {
        'phone_number': '+254733333333',
        'first_name': 'Test'
    }
    
    response = client.post('/accounts/handler/create-user/', incomplete_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    
    if response.status_code == 400:
        print("✓ Correctly rejected incomplete data")
    else:
        print(f"✗ Should have rejected incomplete data")
    
    # Test 5: Non-handler trying to create user
    print("\n--- Test 5: Non-Handler Access (Should Fail) ---")
    
    # Create a regular client user
    regular_user, created = User.objects.get_or_create(
        username='regular_client',
        defaults={
            'phone_number': '+254744444444',
            'email': 'regular@test.com',
            'first_name': 'Regular',
            'last_name': 'User',
            'user_type': 'client',
            'is_verified': True
        }
    )
    if created:
        regular_user.set_password('regularpass123')
        regular_user.save()
    
    # Login as regular user
    client_regular = APIClient()
    login_response = client_regular.post('/accounts/login/', {
        'username': 'regular_client',
        'password': 'regularpass123'
    })
    
    if login_response.status_code == 200:
        token = login_response.data.get('access')
        client_regular.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = client_regular.post('/accounts/handler/create-user/', {
            'phone_number': '+254755555555',
            'first_name': 'Should',
            'last_name': 'Fail',
            'user_type': 'client',
            'password': 'password123'
        })
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.data}")
        
        if response.status_code == 403:
            print("✓ Correctly denied non-handler access")
        else:
            print(f"✗ Should have denied non-handler access")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    
    # Cleanup test users
    print("\nCleaning up test users...")
    User.objects.filter(phone_number__in=[
        '+254711111111', '+254722222222', '+254733333333', 
        '+254744444444', '+254755555555'
    ]).delete()
    print("✓ Cleanup complete")

if __name__ == '__main__':
    test_handler_create_user()
