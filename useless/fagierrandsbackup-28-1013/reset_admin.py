#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fagierrandsbackup.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'admin'
new_password = 'Admin@2026'

try:
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()
    print(f"Password reset successfully for '{username}'!")
    print(f"Username: {username}")
    print(f"Password: {new_password}")
except User.DoesNotExist:
    print(f"User '{username}' does not exist!")
