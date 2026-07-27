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
    'joy': 670, 'muna': 664, 'miyanne': 683, 'rebune': 678,
    'halima': 692, 'trainers': 677, 'kelvin odero': 681,
    'odero kevin': 681,
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
    ('sekani flowers',          '',             'riziki appartments',                           'northside appartments',                        '6.4km',  'johnson wawire'),
    ('yyvonne  - jitihada',     '727111000',    'yyvonne  -jitihada',                           'ku -refferal hospital',                        '19.7km', 'tony sangura'),
    ('rebune international',    '711670387',    'rebune   international',                       'jumia cbd',                                    '4.3km',  'willy masinde'),
    ('rebune international',    '711670387',    'rebune   international',                       'eastleigh   section 3',                        '5.6km',  'willy masinde'),
    ('rebune international',    '711670387',    'eastleigh',                                    'rebune  internationl',                         '5.6km',  'willy masinde'),
    ('halima -dera',            '795118132',    'cianda  mall  - fagi shop',                    'nyayo   house',                                '1.7km',  'johnson wawire'),
    ('gloria   -kitchenware',   '113235433',    'gloria kitchenware   -  almond park   off kilifi close', 'BCNN  SUITES   , Kirwa rd',          '19.8km', 'shadracka tito'),
    ('kelvin odero',            '712445305',    'ministry of lands',                            'kikuyu',                                       '17.3km', 'shadracka tito'),
    ('trainers by sway',        '254140068370', 'kamukunji  busienss   center',                 'eastleigh   section 3',                        '4.1km',  'cyrus ambani'),
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
