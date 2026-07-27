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
    'belizi': 423, 'mtindo': 609, 'wakiarie': 551,
    'avana': 521, 'superfine': 518, 'jazi': 583,
    'gloria': 489, 'almond': 489, 'athiambo': 634,
    'kiatu': 341, 'mepalux': 341, 'meplaux': 341,
    'micheal': 604, 'michael': 604, 'sekani': 385, 'health': 472,
    'chelsea': 452, 'alfa': 649, 'unique': 513, 'andrew': 607,
    'yvonne': 651, 'yyvonne': 651, 'noreen': 656,
    'joy': 670, 'muna': 664, 'miyanne': 683, 'maiyanne': 683,
    'rebune': 678, 'halima': 692, 'trainers': 677,
    'kelvin odero': 681, 'kevin odero': 681,
    'nancy': 659, 'muthoni': 695, 'linet': 699,
    'nm perfumes': 700, 'sandra': 701,
    'rng plaza': 702, 'baddies': 632, 'tange': 679,
    'micheals tom': 703,
    'queens choice': 595, 'queens  choice': 595, 'quees choice': 595,
    'queens-choice': 595, 'queens -rng': 658, 'queens rng': 658, 'queensrng': 658,
    'queens-rng': 658, 'rng  plaza': 702,
    'jitihada': 584,
    'pramukh': 704,
    'joe': 705,
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
scheduled_date = "2026-07-24"

rows = [
    ('noreen',                      '721999686',    'kamukunji  -gecha market',             'mimosa court',                             '4.8km',  'tony sangura'),
    ('noreen',                      '721999686',    'hazina trade centre',                  'mimosa court',                             '4.1km',  'tony sangura'),
    ('queens  choice',              '768887510',    'baraga bookshop',                      'hamza plaza',                              '110m',   'shadrack atito'),
    ('queens  choice',              '768887510',    'hamza plaza',                          'dynamic plaza',                            '6.4km',  'shadrack atito'),
    ('queens  choice',              '768887510',    'stanback  house',                      'baraga    bookshop',                       '6.5km',  'shadrack atito'),
    ('avana  soles',                '702840229',    'kariakor  market',                     'pioneer  - kimathi street',                '3.8km',  'shadrack atito'),
    ('jitihada  -yyvonne',          '794447655',    'jithada bsuiness  centre',             'kiambu road four ways',                    '10.1km', 'willy masinde'),
    ('kiatu   emporium  - mepalux', '733273632',    'meplaux plaza',                        'parkside towers',                          '7.3km',  'cyrus ambani'),
    ('baddies  empire',             '748399605',    'dynamic mall',                         'lavingtone',                               '7.1km',  'cyrus ambani'),
    ('fitbox  - ke',                '759396635',    'kamukunji police   station',           'komarock   phase  3b',                     '12.1km', 'cyrus ambani'),
    ('halima  -dera',               '795118132',    'cianda  -fagi shop',                   'the bazaar',                               '1.7km',  'johnson wawire'),
    ('halima  -dera',               '795118132',    'cianda  -fagi shop',                   'nyanyuki cbas',                            '400m',   'johnson wawire'),
    ('halima  -dera',               '795118132',    'cianda  -fagi shop',                   'nhc   apartment   t-mall',                 '4.3km',  'johnson wawire'),
    ('halima  -dera',               '795118132',    'cianda  -fagi shop',                   'don bosco  catholic   church',             '5.0km',  'johnson wawire'),
    ('halima  -dera',               '795118132',    'cianda  -fagi shop',                   'jp parcel',                                '400m',   'johnson wawire'),
    ('halima  -dera',               '795118132',    'cianda  -fagi shop',                   'ena coach',                                '750m',   'kelvin ndungu'),
    ('halima  -dera',               '795118132',    'cianda  -fagi shop',                   'T-MALL - Lngata',                          '4.3km',  'johnson wawire'),
    ('joe',                         '',             'cianda  -fagi shop',                   'nextgen mall',                             '7.4km',  'daniel nyakundi'),
    ('joy  business',               '718840856',    'westlands  - glory safaris',           'total wangige',                            '13.2km', 'johnson wawire'),
    ('jitihada  -yyvonne',          '794447655',    'jithada bsuiness  centre',             'promenade',                                '6.8km',  'tony sangura'),
    ('queens -rng plaza',           '710617679',    'rng plaza',                            'ngara',                                    '2.1km',  'willy masinde'),
    ('meplaux plaza',               '733273632',    'kiatu meporium',                       'copperative bank inurstrail area',         '8.6km',  'daniel nyakundi'),
    ('noreen',                      '721999686',    'jori maark   ctr-nyamakima',           'sbm   riverside',                          '4.4km',  'shadrack atito'),
    ('noreen',                      '721999686',    'gaebrone   plaza   2nd floor',         'standard charter  - westlands',            '3.8km',  'shadrack atito'),
    ('noreen',                      '721999686',    'ktda   farmers    biulding',           'westalnds  - church road',                 '11.1km', 'tony sangura'),
    ('noreen',                      '721999686',    'eastleigh   - social hall',            'westalnds  - church road',                 '9.7km',  'tony sangura'),
    ('mtindo wear',                 '729620888',    'cianda  -fagi shop',                   'great-rift  shuttle',                      '400m',   'daniel nyakundi'),
    ('mtindo wear',                 '729620888',    'cianda  -fagi shop',                   'kileleshwa',                               '6.7km',  'daniel nyakundi'),
    ('mtindo wear',                 '729620888',    'cianda  -fagi shop',                   'pick up mtaani -gogo mall',                '550m',   'kelvin ndungu'),
    ('halima  -dera',               '795118132',    'cianda  -fagi shop',                   'hh towers',                                '1.5km',  'shadrack atito'),
    ('noreen',                      '721999686',    'dontown towers',                       'baba dogo',                                '9.3km',  'willy masinde'),
    ('noreen',                      '721999686',    'gaebrone   plaza   2nd floor',         'standard charter  - westlands',            '3.8km',  'shadrack atito'),
    ('pramukh plaza',               '702798298',    'pramukh plaza',                        'umoja 1',                                  '9.9km',  'johnson wawire'),
    ('pramukh plaza',               '702798298',    'umoja 1',                              'pramukh',                                  '9.9km',  'johnson wawire'),
    ('baddies  empire',             '748399605',    'dynamic mall',                         'caren hoppersville   aprtment  ngong racecourse', '11.4km', 'tony sangura'),
    ('jitihada  -yyvonne',          '794447655',    'jithada bsuiness  centre',             'lynwood  heights   kiambu road',           '11.0km', 'johnson wawire'),
    ('fitbox  - ke',                '759396635',    'kamukunji police station',             'chema suites  - utawala',                  '18.5km', 'shadrack atito'),
    ('wakiarie business',           '742537182',    'afya centre',                          'ngara',                                    '1.7km',  'daniel nyakundi'),
    ('mtindo wear',                 '729620888',    'cianda  -fagi shop',                   'molo line',                                '1.0km',  'tony sangura'),
    ('mtindo wear',                 '729620888',    'cianda  -fagi shop',                   'ngara',                                    '2.0km',  'shadrack atito'),
    ('mtindo wear',                 '729620888',    'cianda  -fagi shop',                   'narok line',                               '300m',   'tony sangura'),
    ('mtindo wear',                 '729620888',    'cianda  -fagi shop',                   'nuclear (2 parcels)',                       '1.4km',  'tony sangura'),
    ('mtindo wear',                 '729620888',    'cianda  -fagi shop',                   'langata',                                  '10.7km', 'shadrack atito'),
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
