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
    'avana': 521, 'superfine': 518, 'gloria': 489, 'almond': 489,
    'kiatu': 341, 'mepalux': 341, 'meplaux': 341,
    'micheal': 604, 'michael': 604, 'sekani': 385, 'health': 472,
    'chelsea': 452, 'alfa': 649, 'unique': 513, 'andrew': 607,
    'yvonne': 651, 'yyvonne': 651, 'noreen': 656,
    'joy': 670, 'muna': 664, 'miyanne': 683, 'rebune': 678,
    'halima': 692, 'trainers': 677, 'kelvin odero': 681,
    'nancy': 659, 'muthoni': 695, 'linet': 699,
    'nm perfumes': 700, 'sandra': 701, 'rng plaza': 702,
    'baddies': 632, 'tange': 679, 'micheals tom': 703,
    'pramukh': 704, 'joe': 705,
    'genuine kunga': 671, 'harriet': 593, 'ree style': 654,
    'where ke': 706, 'shizz': 707,
    'queens-rng': 658, 'queens rng': 658, 'quees-rng': 658,
    'jitihada': 584,
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
scheduled_date = "2026-07-25"

rows = [
    ('quees choice',                '768887510',    'baraga bookshop',                      'gogo mall  - pick  up mtaani',             '6.2km',  'tony sangura'),
    ('quees choice',                '768887510',    'baraga bookshop',                      'dynamic mall',                             '6.7km',  'tony sangura'),
    ('genuine kunga therapy',       '700797110',    'sunrays   coasmetics',                 'genuine kunga therapy',                    '7.3km',  'daniel nyakundi'),
    ('sunrays cosmetics',           '700797110',    'genuine kunga therapy',                'fedha urban beauty    opp quickmart',      '18.5km', 'daniel nyakundi'),
    ('harriet - new client',        '',             'sunny park appartment  -ngong rd',     'kamiti road',                              '19.9km', 'shadracka tito'),
    ('jitihada  - yyvonne',         '794447655',    'jitihada   business',                  'loresho primary school',                   '7.5km',  'willy masinde'),
    ('kaitu emporium  -mepalux',    '733273632',    'mepalux plaza',                        'mutati road   -parklands',                 '11.3km', 'johnson wawire'),
    ('fitbox   ke  -kamukunji',     '759396635',    'kamukunji police station',             'ndenderu  satge',                          '18.8km', 'tony sangura'),
    ('fitbox   ke  -kamukunji',     '759396635',    'kamukunji police station',             'rng plaza',                                '1.0km',  'tony sangura'),
    ('sunrays cosmetics',           '700797110',    'sunrays   coasmetics',                 'circle    mall kilimani',                  '5.0km',  'johnson wawire'),
    ('belizi fashions',             '748399605',    'kbs agrage  - eastleigh',              'star court    syokimau',                   '19.2km', 'willy masinde'),
    ('rng  plaza   -queens',        '710617679',    'rng plaza',                            'langat dog unit',                          '10.0km', 'johnson wawire'),
    ('noreen',                      '721999686',    'hazina trade centre',                  'karen ndege road',                         '17.4km', 'daniel nyakundi'),
    ('sunrays cosmetics',           '700797110',    'sunrays   coasmetics',                 'kpa  flats south -c',                      '8.8km',  'shadracka tito'),
    ('halima - dera',               '795118132',    'cianda - fagi shop',                   'narok line',                               '300m',   'shadracka tito'),
    ('halima  - dera',              '795118132',    'cianda - fagi shop',                   'lodwa jp parcels',                         '400m',   'shadracka tito'),
    ('halima - dera',               '795118132',    'cianda - fagi shop',                   'maralal  safaris',                         '1.5km',  'shadracka tito'),
    ('halima -dera',                '795118132',    'cianda - fagi shop',                   'lopha travellers',                         '700m',   'shadracka tito'),
    ('quees-rng',                   '710617679',    'cianda - fagi shop',                   'eastleigh',                                '4.5km',  'johnson wawire'),
    ('harriet - new client',        '',             'city market',                          'oj -ruiru',                                '23km',   'willy masinde'),
    ('chelsea flowers',             '',             'city market',                          'coptic hospital',                          '7.5km',  'willy masinde'),
    ('ree styles',                  '',             'cianda  -fagi shop',                   'naekan sacco',                             '1.0km',  'johnson wawire'),
    ('ree styles',                  '',             'cianda -fagi shop',                    'gikomba behind -equity bank',              '500m',   'johnson wawire'),
    ('baddies empire',              '',             'dyna,mic mall',                        'winchester   garden kilelshwa',            '7.5km',  'johnson wawire'),
    ('where ke',                    '714352229',    'sonalux house',                        'jabavu court',                             '6.4km',  'willy masinde'),
    ('shizz thrift',                '790182722',    'philadelphia house',                   'jabavu court',                             '5.2km',  'willy masinde'),
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
