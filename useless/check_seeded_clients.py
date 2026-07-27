import os
import sys
import django

sys.path.insert(0, '/home3/distinc3/fagiserver.fagtone.com/fagierrandsbackup')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fagierrandsbackup.settings')
django.setup()

from accounts.models import User

seeded = [
    'alfafashions','alinaridge','baddiesempire','chelsea','climeshdesigns',
    'fashionfix','genuinekunga','halimafashions','homeoftrainer','joybusiness',
    'kelvindungu','kimathihouse','kwabrown','kwamwalimu','linayarn',
    'mercyscott','miyannegifts','mtindongara','munaflowers','nancylisters',
    'nashique','niapetals','niapetalsnew','nkirobi','nolanskids',
    'nooreen','odero','oderovictor','queensrng','rebune',
    'reestyle','tangecollect','tangecollection','tonysangura','trainersbysway',
    'vallaries','villablooms','willyriverside','yellowpages','yvonnejitihada'
]

existing = list(User.objects.filter(username__in=seeded).values_list('username', flat=True))
not_found = [u for u in seeded if u not in existing]

print(f"\nIN DATABASE ({len(existing)}):")
for u in sorted(existing):
    print(f"  + {u}")

print(f"\nNOT IN DATABASE ({len(not_found)}):")
for u in sorted(not_found):
    print(f"  - {u}")
