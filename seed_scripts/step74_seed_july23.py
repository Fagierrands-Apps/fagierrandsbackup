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
    'yvonne': 651, 'yyvonne': 651, 'yyvone': 651, 'yvvone': 651,
    'noreen': 656, 'joy': 670, 'muna': 664, 'miyanne': 683, 'maiyanne': 683,
    'rebune': 678, 'halima': 692, 'halma': 692, 'trainers': 677,
    'kelvin odero': 681, 'kevin odero': 681, 'odero kevin': 681,
    'nancy': 659, 'muthoni': 695, 'lucy': 694, 'linet': 699,
    'nm perfumes': 700, 'sandra': 701,
    'rng plaza': 702, 'rngplaza': 702,
    'baddies': 632, 'tange': 679,
    'micheals tom': 703, 'michaels tom': 703,
    'jitihada': 651,
}

riders = {
    'shadrack': 477, 'shadrcak': 477, 'shadracka': 477, 'shadrack atito': 477,
    'cyrus': 375, 'johnson': 374, 'willy': 403,
    'jesse': 109, 'daniel': 310, 'tony': 661,
    'kelvin': 667, 'kevin': 667, 'nyakundi': 310,
    'cyrs': 375,
}

def get_id(name, mapping):
    name = str(name).lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-07-23"

rows = [
    ('rng plaza',               '745158721',    'rng plaza',                                    'tefillah residence  - thindigua',              '12.2km', 'willy masinde'),
    ('sunrays flora house',     '700797110',    'sunrays  - flora house',                       'impala auto spares indurstrial area',           '3.9km',  'tony sangura'),
    ('baddies empire',          '748399605',    'dynamic mall',                                 'cozy haven pride - thidigua',                  '13.0km', 'daniel nyakundi'),
    ('wakiarie business',       '74537181',     'afya centre',                                  'kileleshwa',                                   '7.4km',  'shadracka atito'),
    ('baddies empire',          '748399605',    'dynamic mall',                                 'kariakor market',                              '2.4km',  'johnson wawire'),
    ('tange collection',        '714348056',    'tsavo sunset-thindigua',                       'emperor  plaza  - kenyatta avenue',            '11.8km', 'daniel nyakundi'),
    ('tange collection',        '',             'emperor  plaza  - kenyatta avenue',            'tsavo sunset   - thindigua',                   '11.8km', 'cyrus ambani'),
    ('yyvone  - jitihada',      '727111000',    'jitihada business centre',                     'madaraka estate',                              '4.9km',  'johnson wawire'),
    ('fitbox-ke',               '759396635',    'kamukunji police station',                     'zion luxury appartments -kitengela',           '31.5km', 'tony sangura'),
    ('sunrays flora house',     '700797110',    'sunrays  - flora house',                       'shauri moyo   - bama market',                  '3.7km',  'shadracka atito'),
    ('noreen',                  '721999686',    'eastleigh  - social hall',                     'ruaka',                                        '15.1km', 'johnson wawire'),
    ('kevin odero',             '717246434',    'west park suites',                             'ack garden house  -  1st ngong avenue',        '4.4km',  'shadracka atito'),
    ('alfa fashions',           '796736969',    'rng plaza',                                    'duldul phase 1 -godown',                       '12.4km', 'cyrus ambani'),
    ('sunrays flora house',     '700797110',    'sunrays  - flora house',                       'brookside gardens',                            '6.3km',  'shadracka atito'),
    ('sunrays flora house',     '700797110',    'sunrays  - flora house',                       'mtito andei   -kilimani',                      '4.0km',  'shadracka atito'),
    ('noreen',                  '721999686',    'royal palms   mall-  ronald ngala rd',         'hesed   africa foundation -kilimani',          '5.4km',  'shadracka atito'),
    ('trainers  by sway',       '254140068370', 'kamukunji business centre',                    'eastleigh- amal  plaza',                       '3.4km',  'tony sangura'),
    ('trainers  by sway',       '254140068370', 'kamukunji business centre',                    'ruiru prison    bike stage',                   '23.2km', 'tony sangura'),
    ('baddies empire',          '748399605',    'dynamic mall',                                 'shangrila residency  -westlands',              '5.8km',  'daniel nyakundi'),
    ('super fine beddings',     '',             'bestlady  -ronald ngala',                      'uthiru',                                       '22.2km', 'shadracka atito'),
    ('raven',                   '792293948',    'cjs koinange street',                          'shepherds  ruiru pub',                         '25.6km', 'johnson wawire'),
    ('halma dera',              '795118132',    'cianda  -fagi shop',                           'nyayo house',                                  '1.7km',  'cyrus ambani'),
    ('mtindo wear',             '726620888',    'cianda  -fagi shop',                           'harmony    court jamuhuri',                    '10.7km', 'cyrus ambani'),
    ('yvvone -jitihada',        '727111000',    'cianda  -fagi shop',                           'kilimani',                                     '5.8km',  'cyrus ambani'),
    ('halima -dera',            '795118132',    'cianda  -fagi shop',                           'city shuttle',                                 '400m',   'kelvin ndungu'),
    ('halima -dera',            '795118132',    'cianda  -fagi shop',                           'muranga parcel courier',                       '1.0km',  'kelvin ndungu'),
    ('halima -dera',            '795118132',    'cianda  -fagi shop',                           'narok line',                                   '1.0km',  'kelvin ndungu'),
    ('halima -dera',            '795118132',    'cianda  -fagi shop',                           'indimanje parcels',                            '900m',   'kelvin ndungu'),
    ('mtindo wear',             '726620888',    'cianda  -fagi shop',                           'pick up mtaai - gogo mall',                    '550m',   'kelvin ndungu'),
    ('micheals tom mboya',      '794775593',    'micheals tom mboya',                           'utwala  airways -mihango',                     '24.1km', 'daniel nyakundi'),
    ('halima dera',             '795118132',    'cianda  -fagi shop',                           'nyanyuki cabs',                                '400m',   'shadracka atito'),
    ('halima dera',             '795118132',    'cianda  -fagi shop',                           'the bazaar',                                   '500m',   'shadracka atito'),
    ('gloria jeruto',           '113235433',    'hazina  towers',                               'almond park',                                  '6.1km',  'cyrus ambani'),
    ('unique trend',            '762925006',    'cianda  -fagi shop',                           'kilimani',                                     '5.9km',  'willy masinde'),
    ('halima dera',             '795118132',    'cianda  -fagi shop',                           'ena coach (2 parcels)',                         '750m',   'kelvin ndungu'),
    ('halima dera',             '795118132',    'cianda  -fagi shop',                           'metro trans',                                  '800m',   'kelvin ndungu'),
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
