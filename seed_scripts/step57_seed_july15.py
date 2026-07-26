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

def parse_value(v):
    try:
        return float(''.join(c for c in str(v) if c.isdigit() or c == '.'))
    except:
        return 0

clients = {
    'sunrays': 372, 'classic': 332, 'fitbox': 338, 'fit box': 338,
    'adult': 586, 'belizi': 423, 'mtindo  wear': 657, 'mtindo': 609,
    'queens': 595, 'wakiarie': 551, 'avana': 521, 'superfine': 518,
    'jazi': 583, 'gloria': 489, 'almond': 489, 'athiambo': 634,
    'kiatu': 341, 'micheal': 604, 'michael': 604, 'sekani': 385,
    'health': 472, 'unique': 513,
    'chelsea': 452, 'alfa': 649, 'rng': 649, 'yvonne': 651,
    'kwa brown': 652, 'alina': 655, 'nooreen': 656, 'noreen': 656,
    'queensrng': 658, 'nancy': 659, 'kwa mwalimu': 660,
    'odero': 662, 'climesh': 663, 'muna': 664,
    'home of trainer': 665, 'villa blooms': 666,
    'nolans': 668, 'lina yarn': 669, 'joy': 670,
    'genuine kunga': 671, 'baddies': 632,
    'mercy': 673, 'vallaries': 674, 'nia petals': 675,
    'willy-riverside': 676, 'trainers': 677,
    'northside': 385,  # sekani = northside apartments
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374,
    'willy': 403, 'jesse': 109, 'daniel': 310,
    'tony': 661, 'kelvin': 667, 'nyakundi': 310,
}

def get_id(name, mapping):
    name = str(name).lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-07-15"

rows = [
    ('wakiarie business',                           '742537182', 'afya centre',                              'westlands',                                            '3000ksh', '5.3km',  'johnson wawire'),
    ('sunrays   - flora house',                     '700797110', 'sunrays   cosmetics  -flora house',        'ngara equity',                                         '3000ksh', '1.5km',  'tony sangura'),
    ('mercy scott- new client',                     '721736140', 'mathais supermarket',                      'ngara',                                                '5000ksh', '4.0km',  'johnson wawire'),
    ('sekani -northside apartment',                 '118260620', 'northside aparment',                       'nextgen apartment',                                    '4000ksh', '9.3km',  'willy masinde'),
    ('kiatu emporium   -    mepalux',               '733273632', 'kamkunji',                                 'rhaphta road westlands',                               '4500ksh', '7.4km',  'shadrack atito'),
    ('yvonne jitihada',                             '727111000', 'jitihada',                                 'kileleshwa dikdik gardens',                            '3500ksh', '7.4km',  'johnson wawire'),
    ('fit box',                                     '759396635', 'kamkunji',                                 'civil servant housing scheme kiambu',                  '4500ksh', '14.8km', 'shadrack atito'),
    ('athiambos thrifts',                           '112012425', 'hakati business center',                   'westlands',                                            '2000ksh', '5.0km',  'johnson wawire'),
    ('unique collection',                           '757609903', 'Accra road, accra hotel building second',  'jeevanjee jumia',                                      '10000ksh','2km',    'willy masinde'),
    ('northside apartment',                         '118260620', 'northside aparment',                       'eastliegh',                                            '0ksh',    '5.6km',  'nyakundi'),
    ('baddies   empire    -dynamic    mall',        '759535915', 'dynamic  mall',                            'plainsville',                                          '2000ksh', '6.0km',  'johnson wawire'),
    ('mtindo wear  - cianda mall  (fagi)',           '726620888', 'cianda mall  - mfagano street',            'pickup mtaani',                                        '0ksh',    '550m',   'tony sangura'),
    ('mtindo wear  - cianda mall  (fagi)',           '726620888', 'cianda mall  - mfagano street',            '2nk parcel',                                           '0ksh',    '800m',   'tony sangura'),
    ('mtindo wear  - cianda mall  (fagi)',           '726620888', 'cianda mall  - mfagano street',            'mlolongo',                                             '300ksh',  '19.9km', 'tony sangura'),
    ('baddies   empire    -dynamic    mall',        '759535915', 'dynamic  mall',                            'Dennis Garden Apartment',                              '6000ksh', '6.6km',  'johnson wawire'),
    ('fit box',                                     '759396635', 'kamkunji',                                 'Prittlane court 3',                                    '2000ksh', '10.3km', 'johnson wawire'),
    ('vallaries collection-new client',             '708203462', 'cianda mall  - mfagano street',            'Killimani kirichwa road Sapphire Court House Number B307','4000ksh','6.7km', 'johnson wawire'),
    ('fit box',                                     '759396635', 'civil servant housing scheme kiambu',      'kamkunji',                                             '4500ksh', '14.8km', 'shadrack atito'),
    ('avana soles',                                 '712083313', 'kariakor market',                          'laibon rd   nrbi -harambee   school buruburu',         '5000ksh', '8.7km',  'cyrus ambani'),
    ('Michaels',                                    '794775593', 'michaels',                                 'ruiru astro',                                          '3500ksh', '23.7km', 'cyrus ambani'),
    ('Nia Petals, Cianda House',                    '713777513', 'Nia Petals, Cianda House',                 'Drop off Dunhill Towers Westlands',                    '4000ksh', '4.2km',  'willy masinde'),
    ('athiambos thrifts',                           '112012425', 'hakati business center',                   'westlands',                                            '1500ksh', '5.0km',  'nyakundi'),
    ('gloria -kitchenware almond park',             '113235433', 'almond park -kilif close',                 '6th parklands,mwamba road',                            '6000ksh', '10.3km', 'cyrus ambani'),
    ('health classic',                              '722995300', 'health classic -next gen',                 'naivas kimathi street',                                '3000ksh', '6.2km',  'shadrack atito'),
    ('health classic',                              '722995300', 'health classic -next gen',                 'Rosslyn green lane, last house with wooden gate.',     '6000ksh', '15.2km', 'shadrack atito'),
    ('gloria -kitchenware almond park',             '113235433', 'almond park -kilif close',                 'fairfield gardens katani road,syokimau',               '5000ksh', '17.4km', 'tony sangura'),
    ('willy-riverside',                             '708632359', 'riverside',                                'nyayo statium',                                        '3500ksh', '7.2km',  'willy masinde'),
    ('yvonne jitihada',                             '727111000', 'jitihada',                                 'dohnhom',                                              '7500ksh', '10.7km', 'johnson wawire'),
    ('Trainers by sway',                            '1140068370','kamkunji',                                 'bbs mall eastliegh',                                   '4500ksh', '3.0km',  'shadrack atito'),
]

success, skipped = 0, 0
for client, phone, pickup, dropoff, value, dist, rider in rows:
    client_id = get_id(client, clients)
    rider_id = get_id(rider, riders)
    if not client_id or not rider_id:
        print(f"SKIP: client='{client}'({client_id}) rider='{rider}'({rider_id})")
        skipped += 1
        continue
    price = calc_price(dist)
    km = parse_km(dist)
    est_val = parse_value(value)
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
            {km}, true, {est_val}
        ) RETURNING id, client_id, assistant_id, price;
    """)
    success += 1

print(f"\nDone: {success} inserted, {skipped} skipped for {scheduled_date}")
