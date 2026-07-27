import subprocess
from datetime import datetime

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

def calc_price(km_str):
    try:
        s = str(km_str).lower().strip()
        if 'km' in s: km = float(s.replace('km','').strip())
        elif 'm' in s: km = float(s.replace('m','').strip()) / 1000
        else: km = float(s)
        return 200 if km <= 7.5 else round(200 + (km - 7.5) * 23)
    except:
        return 200

def parse_km(s):
    try:
        s = str(s).lower().strip()
        if 'km' in s: return float(s.replace('km','').strip())
        if 'm' in s: return round(float(s.replace('m','').strip()) / 1000, 3)
        return float(s)
    except:
        return 0

clients = {
    'sunrays': 372, 'classic': 332, 'fitbox': 338, 'adult': 586,
    'belizi': 423, 'mtindo': 609, 'queens': 595, 'wakiarie': 551,
    'avana': 521, 'superfine': 518, 'jazi': 583, 'jazy': 583,
    'gloria': 489, 'almond': 489, 'athiambo': 634, 'kiatu': 341,
    'micheal': 604, 'michael': 604, 'sekani': 385, 'health': 472,
    'chelsea': 452, 'alfa': 649, 'unique': 513, 'andrew': 607,
    'yvonne': 651, 'yyvonne': 651, 'noreen': 656, 'norren': 656,
    'joy': 670, 'muna': 664, 'miyanne': 683, 'maiyanne': 683,
    'rebune': 678, 'halima': 692, 'trainers': 677, 'kelvin odero': 681,
    'nancy': 659, 'muthoni': 695, 'lucy': 694, 'linet': 699,
    'nm perfumes': 700, 'nmperfumes': 700, 'sandra': 701,
}

riders = {
    'shadrack': 477, 'shadrcak': 477, 'shadracka': 477,
    'cyrus': 375, 'johnson': 374, 'willy': 403,
    'jesse': 109, 'daniel': 310, 'tony': 661,
    'kelvin': 667, 'kevin': 667, 'nyakundi': 310,
}

def get_id(name, mapping):
    name = str(name).lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-07-22"

rows = [
    ('halima -dera',                    '795118132',    'cianda  mall  - fagi shop',            'enabled shuttle',                              '1.1km',  'johnson wawire'),
    ('halima -dera',                    '795118132',    'cianda  mall  - fagi shop',            'pick up mtaani  - gogo mall',                  '550m',   'johnson wawire'),
    ('sunrays  cosmetics - flora house','700797110',    'sunrays   cosmetics  - flora house',   'qwetu  student residency',                     '6.7km',  'daniel nyakundi'),
    ('trainers by sway',                '254140068370', 'kamukunji  busienss   center',         'ngara',                                        '900m',   'cyrus ambani'),
    ('maiyanne   gifts',                '729228868',    'maiyanne gifts   -city market',        'reinsurrance    plaza',                        '900m',   'kelvin ndungu'),
    ('halima -dera',                    '795118132',    'cianda  mall  - fagi shop',            'ena coach ( 5 parcels)',                        '750m',   'tony sangura'),
    ('halima -dera',                    '795118132',    'cianda  mall  - fagi shop',            'enabled shuttle',                              '1.1km',  'tony sangura'),
    ('halima -dera',                    '795118132',    'cianda  mall  - fagi shop',            'super metro',                                  '600m',   'tony sangura'),
    ('halima -dera',                    '795118132',    'cianda  mall  - fagi shop',            'latema',                                       '700m',   'tony sangura'),
    ('halima -dera',                    '795118132',    'cianda mall - fagi shop',              'manyanja',                                     '8.6km',  'tony sangura'),
    ('noreen',                          '721999686',    'hirson plaza  - biashara street',      'amboseli lane',                                '7.9km',  'johnson wawire'),
    ('nm perfumes',                     '710515777',    'kimathi house   3rd floor',            'viraj    millenium   killeshwa',                '4.4km',  'daniel nyakundi'),
    ('nm perfumes',                     '710515777',    'kimathi house   3rd floor',            'rivers edge   house',                          '21.3km', 'daniel nyakundi'),
    ('trainers by sway',                '254140068370', 'kamukunji  busienss   center',         '7th day adventist   church',                   '23.2km', 'cyrus ambani'),
    ('halima -dera',                    '795118132',    'cianda  mall  - fagi shop',            'old mombasa road',                             '12.9km', 'shadracka tito'),
    ('halima -dera',                    '795118132',    'cianda  mall  - fagi shop',            'south b',                                      '4.3km',  'shadracka tito'),
    ('avana soles',                     '702840229',    'kariakor   market',                    'indurstrail area -impala   auto spares',        '4.2km',  'shadracka tito'),
    ('sunrays  cosmetics - flora house','700797110',    'sunrays   cosmetics  - flora house',   'green field   ,savan rd    donholm',            '9.9km',  'willy masinde'),
    ('sunrays  cosmetics - flora house','700797110',    'sunrays   cosmetics  - flora house',   'maa hotel and suits    -hurlingham',            '3.9km',  'willy masinde'),
    ('wakiarie businesss',              '74537181',     'afya centre',                          'nairobi west',                                 '6.2km',  'johnson wawire'),
    ('joy  business',                   '718840856',    'jethwa mansion',                       'westlands   -raphta rd',                       '4.8km',  'johnson wawire'),
    ('joy  -business',                  '718840856',    'jethwa mansion',                       'westlands   -raphta rd',                       '4.8km',  'johnson wawire'),
    ('mtindo  wear',                    '729620888',    'cianda-  fagi shop',                   'chania genesis',                               '900m',   'johnson wawire'),
    ('mtindo  wear',                    '729620888',    'cianda-  fagi shop',                   'chania   -thika  route',                       '900m',   'johnson wawire'),
    ('mtindo  wear',                    '729620888',    'cianda-  fagi shop',                   'gogo mall',                                    '550m',   'johnson wawire'),
    ('avana soles',                     '702840229',    'avana karaikaor',                      'super metro - ntional archives',               '2.6km',  'cyrus ambani'),
    ('sunrays  cosmetics - flora house','700797110',    'sunrays   cosmetics  - flora house',   'highrise',                                     '6.4km',  'cyrus ambani'),
    ('halima -dera',                    '795118132',    'cianda  mall  - fagi shop',            'riverside   westalnds',                        '6.1km',  'tony sangura'),
    ('muthoni thrift',                  '',             'philadephia',                          'shauri moyo',                                  '3.3km',  'tony sangura'),
    ('sandra - new client',             '',             'cianda mall-fagi shop',                'dynamic mall',                                 '450m',   'shadracka tito'),
    ('sandra - new client',             '',             'dynamic mall',                         'kasarni  sunton',                              '16.2km', 'shadracka tito'),
]

success, skipped = 0, 0
for client, phone, pickup, dropoff, dist, rider in rows:
    client_id = get_id(client, clients)
    rider_id = get_id(rider, riders)
    if not client_id or not rider_id:
        print(f"SKIP: client='{client}'({client_id}) rider='{rider}'({rider_id})")
        skipped += 1
        continue
    price = calc_price(dist)
    km = parse_km(dist)
    p = pickup.strip().replace("'", "''")
    d = dropoff.strip().replace("'", "''")
    psql(f"""
        INSERT INTO orders_order (
            title, description, pickup_address, delivery_address,
            contact_number, scheduled_date, price, status,
            created_at, updated_at, completed_at,
            client_id, assistant_id, order_type_id,
            distance, price_finalized, estimated_value
        ) VALUES (
            'Pickup & Delivery Order', '{p} to {d}',
            '{p}', '{d}', '{phone}', '{scheduled_date}',
            {price}, 'completed', '{now}', '{now}', '{now}',
            {client_id}, {rider_id}, 2,
            {km}, true, 0
        ) RETURNING id, client_id, assistant_id, price;
    """)
    success += 1

print(f"\nDone: {success} inserted, {skipped} skipped for {scheduled_date}")
