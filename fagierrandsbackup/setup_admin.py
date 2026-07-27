"""
Run on Render shell or locally to create/activate a superuser.
Reads credentials from env vars:
  DJANGO_SUPERUSER_USERNAME (default: admin)
  DJANGO_SUPERUSER_EMAIL
  DJANGO_SUPERUSER_PASSWORD (required)
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fagierrandsbackup.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@fagierrands.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "Admin@2026")

user, created = User.objects.get_or_create(username=username, defaults={"email": email})
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()

print(f"{'Created' if created else 'Updated'} superuser: {username}")
