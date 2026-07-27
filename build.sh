#!/usr/bin/env bash
set -o errexit

echo "🚀 Starting Render deployment..."

# Navigate to Django project directory
cd fagierrandsbackup

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

echo "✅ Deployment complete!"

# Create or activate superuser
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@fagierrands.com'})
user.set_password('Admin@2026')
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()
print('Superuser created' if created else 'Superuser updated')
"
