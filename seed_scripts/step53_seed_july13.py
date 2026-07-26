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
    'sunrays': 372, 'classic': 332, 'fitbox': 338, 'adult': 586,
    'belizi': 423, 'mtindo  wear': 657, 'mtindo': 609,
    'queens': 595, 'wakiarie': 551, 'avana': 521,
    'jazi': 583, 'jazy': 583, 'gloria': 489, 'almond': 489,
    'athiambo': 634, 'kiatu': 341, 'micheal': 604,
    'chelsea': 452, 'alfa': 649, 'rng': 649,
    'yvonne': 651, 'kwa brown': 652, 'nkirobi': 653,
    'alina': 655, 'nooreen': 656, 'noreen': 656,
    'queensrng': 658, 'nancy': 659, 'kwa mwalimu': 660,
    'odero': 662, 'climesh': 663,
    'muna': 664, 'home of trainer': 665, 'villa blooms': 666,
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374,
    'willy': 403, 'jesse': 109, 'daniel': 310,
    'tony': 661, 'kelvin': 667,
}

def get_id(name, mapping):
    name = str(name).lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-07-13"

rows = [
    ('alfa fashiosn  - rng plaza',              '713064041', 'alfa fashions -rng plaza',             'south c   -west   court house',            '2500ksh', '6.9km',  'tony sangura'),
    ('alfa fashiosn  - rng plaza',              '713064041', 'south c  -west court   house',         'alfa fashions  - rng plaza',               '3000ksh', '6.9km',  'tony sangura'),
    ('queens  choice  - hakati',                '768887510', 'queens  choice  - hakati',             'lumumba drive',                            '500ksh',  '12.4km', 'willy masinde'),
    ('adult  room-starmall',                    '106205106', 'adult room  -starmall',                'kirigiti kiambu',                          '1500ksh', '15.2km', 'shadrack atito'),
    ('muna  flowers  -  city markt',            '724906221', 'muna flowers  -city market',           'optiven',                                  '2500ksh', '15.2km', 'cyrus ambani'),
    ('noreen',                                  '721999686', 'towhid   mall',                        'harambee  sacco  -harambee avenue',        '1500ksh', '4.7km',  'daniel nyakundi'),
    ('queens  choice  - hakati',                '768887510', 'queens  choice  - hakati',             'alba appartments    wanyee rd',            '1500ksh', '9.7km',  'willy masinde'),
    ('queens  choice  - hakati',                '768887510', 'queens  choice  - hakati',             'buruburu  phase   4 - rasetta rd',         '1500ksh', '7.8km',  'willy masinde'),
    ('mtindo wear  - hakati',                   '726620888', 'mtindo wear-hakati',                   'westalnds  -standard   chatered hq',       '1500ksh', '5.7km',  'willy masinde'),
    ('noreen',                                  '721999686', 'kamukunji   -ngecha   market',         'total  -kitsuru',                          '2500ksh', '10.5km', 'tony sangura'),
    ('belizi  fashions',                        '769986885', 'cianda mall',                          'lavender   heights',                       '1000ksh', '12.7km', 'shadrack atito'),
    ('sunrays -flora house',                    '700797110', 'sunrays  -flora house',                'naivas   supermarket   -south c',          '1000ksh', '7.5km',  'shadrack atito'),
    ('sunrays -flora house',                    '700797110', 'sunrays  -flora house',                'seefar appartments   , highrise mbagathi  way','1500ksh','6.6km','shadrack atito'),
    ('home of trainer -kamukunji business centre','254240068370','home of trainer  -kamukunji   business centre','moonlight academy    -dagoretti','4500ksh','13.8km','daniel nyakundi'),
    ('home of trainer -kamukunji business centre','254240068370','moonlight academy  -dagorettu',    'home of trainer   -kamukunji  business cnetre','4500ksh','13.8km','daniel nyakundi'),
    ('biashara street  - villa blooms',         '116682365', 'biashara   street',                    'blixen   court karen',                     '2500ksh', '14.0km', 'willy masinde'),
    ('kiatu emporium   -    mepalux',           '733273632', 'royal palm    -ronald ngara',          'runda mumwe',                              '2000ksh', '12.4km', 'cyrus ambani'),
    ('sunrays -flora house',                    '700797110', 'sunrays  -flora house',                'green court  business centre',             '1500ksh', '34m',    'kelvin  ndungu'),
    ('sunrays -flora house',                    '700797110', 'sunrays  -flora house',                'merchant square   -riverside',             '1500ksh', '5.0km',  'shadrack atito'),
    ('wakiarie  business',                      '742537182', 'afya centre',                          'kileleshwa',                               '2500ksh', '7.3km',  'tony sangura'),
    ('belizi  fashions',                        '790183972', 'iconinc  plaza',                       'uganda house',                             '1500ksh', '750m',   'shadrack atito'),
    ('adultroom',                               '106205106', 'adultroom -starmall',                  'trm',                                      '2500ksh', '0km',    'tony sangura'),
    ('belizi  fashions',                        '790183972', 'iconinc  plaza',                       'bus station',                              '1500ksh', '2.2km',  'shadrack atito'),
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
