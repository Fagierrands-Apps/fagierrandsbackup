import os
import sys
import django

sys.path.insert(0, '/home3/distinc3/fagiserver.fagtone.com/fagierrandsbackup')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fagierrandsbackup.settings')
django.setup()

from django.utils import timezone
from accounts.models import User

now = timezone.now()
users = User.objects.filter(
    user_type__in=['user', 'client'],
    created_at__year=now.year,
    created_at__month=now.month
).order_by('created_at')

print(f"\nClients registered in {now.strftime('%B %Y')}: {users.count()}")
print(f"{'#':<4} {'Username':<20} {'Email':<30} {'Phone':<15} {'Joined'}")
print('-' * 90)

for i, u in enumerate(users, 1):
    print(f"{i:<4} {u.username:<20} {u.email:<30} {str(u.phone_number or ''):<15} {u.created_at.strftime('%Y-%m-%d %H:%M')}")
