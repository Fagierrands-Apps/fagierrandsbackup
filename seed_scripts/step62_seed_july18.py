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
    'yvonne': 651, 'noreen': 656, 'norren': 656, 'nooreen': 656,
    'joy': 670, 'muna': 664, 'miyanne': 683, 'rebune': 678,
    'halima': 692, 'rand landings': 693,
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
scheduled_date = "2026-07-18"

# (client, phone, pickup, dropoff, dist, rider)
rows = [
    ('avana soles',         '702840229',    'kariokor',                             'fourways',                             '9.3km',  'johnson wawire'),
    ('halima dera',         '795118132',    'cianda mall',                          'north rift',                           '350m',   'Willy masinde'),
    ('halima dera',         '795118132',    'cianda mall',                          'supermetro',                           '600m',   'Willy masinde'),
    ('halima dera',         '795118132',    'cianda mall',                          'ena coach',                            '750m',   'Willy masinde'),
    ('halima dera',         '795118132',    'cianda mall',                          'kentmere club',                        '22.4km', 'Johnson wawire'),
    ('halima dera',         '795118132',    'cianda mall',                          'mackos parcel(nnus)',                  '750m',   'Johnson Wawire'),
    ('halima dera',         '795118132',    'cianda mall',                          'kirinyaga road',                       '1.4km',  'Willy masinde'),
    ('Sekani flowers',      '710617679',    'city market',                          'green apartments usiu',                '12.2km', 'Cyrus Ambani'),
    ('Queens',              '710617679',    'rng',                                  'Kileleshwa',                           '6.8km',  'Johnson Wawire'),
    ('Queens',              '710617679',    'rng',                                  'parklands',                            '4.3km',  'Cyrus Ambani'),
    ('Noreen',              '721999686',    'Kamkunji',                             'Kigwa kiambu road',                    '10.7km', 'Daniel nyakundi'),
    ('Yvonne jitihada',     '727111000',    'Jitihada',                             'Equity afya juja',                     '30.6km', 'Cyrus Ambani'),
    ('Adult room',          '106205106',    'Sawa mall',                            'Kanyariri',                            '16.9km', 'Shadrack atito'),
    ('Halima dera',         '795118132',    'Cianda mall',                          'Bomet parcel (nnus)',                  '900m',   'Johnson Wawire'),
    ('Adult room',          '106205106',    'Sawa mall',                            'Naivas githurai 44',                   '14.6km', 'Johnson Wawire'),
    ('Sunrays',             '700797110',    'Sunrays-flora',                        'Genuine kunga',                        '7.3km',  'Tony sangura'),
    ('Sunrays',             '700797110',    'Sunrays-flora',                        'South  c',                             '7.4km',  'Tony Sangura'),
    ('Sunrays',             '700797110',    'Sunrays-flora',                        'South b',                              '5.0km',  'Daniel nyakundi'),
    ('Sunrays-flora',       '700797110',    'Sunrays-flora',                        'Ngara civil servant',                  '4.2km',  'Daniel nyakundi'),
    ('Sunrays',             '700797110',    'Sunrays-flora',                        '3rd parklands',                        '4.2km',  'Johnson Wawire'),
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
