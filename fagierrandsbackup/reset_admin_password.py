#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fagierrandsbackup.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Change these values
username = 'admin'  # Your admin username
new_password = 'NewPassword123!'  # Your new password

try:
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()
    print(f"Password changed successfully for user: {username}")
except User.DoesNotExist:
    print(f"User '{username}' not found. Creating new superuser...")
    User.objects.create_superuser(username=username, email='admin@example.com', password=new_password)
    print(f"Superuser '{username}' created successfully")
