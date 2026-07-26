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
    'mtindo  wear': 657, 'mtindo': 609, 'queens  - rng': 658, 'queensrng': 658,
    'wakiarie': 551, 'avana': 521, 'superfine': 518,
    'jazi': 583, 'jazy': 583, 'gloria': 489, 'almond': 489,
    'athiambo': 634, 'andrew': 607, 'kiatu': 341,
    'chelsea': 452, 'alfa': 649, 'rng': 649,
    'yellow pages': 650, 'yvonne': 651,
    'kwa brown': 652, 'nkirobi': 653, 'ree style': 654,
    'alina': 655, 'nooreen': 656, 'noreen': 656,
    'nancy': 659, 'kwa mwalimu': 660,
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374, 'johnsons': 374,
    'willy': 403, 'jesse': 109, 'daniel': 310,
    'tony': 661,
}

def get_id(name, mapping):
    name = str(name).lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-07-10"

rows = [
    ('sunrays -  flora house',          '700797110', 'sunrays  flora house  - cosmetics',    'south c   green valley  plaza',                '3500ksh', '7.4km',  'shadrack atito'),
    ('avana soles  -kariakor  market',  '702840229', 'avana soles - kariakor market',        'kmoss  - platinum plaza',                      '2000ksh', '6.2km',  'johnsons wawire'),
    ('noreen closets',                  '721999686', 'ktda  farmers biulding',               'horn international',                           '3500ksh', '7.0km',  'shadrack atito'),
    ('sunrays -  flora house',          '700797110', 'sunrays  flora house  - cosmetics',    'grand midtown ngara',                          '1500ksh', '2.4km',  'johnsons wawire'),
    ('mtindo  wear',                    '726620888', 'budget wear    ronald ngara',          'gogo mall  - pick upmtaani',                   '1500ksh', '1.3km',  'willy masinde'),
    ('mtindo  wear',                    '726620888', 'budget wear    ronald ngara',          'dyanmic mall',                                 '1500ksh', '1.1km',  'willy masinde'),
    ('mtindo  wear',                    '726620888', 'budget wear    ronald ngara',          'gallant mall',                                 '1500ksh', '4.9km',  'willy masinde'),
    ('mtindo  wear',                    '726620888', 'budget wear    ronald ngara',          'neo residency    lavington',                   '1500ksh', '8.3km',  'willy masinde'),
    ('mtindo  wear',                    '726620888', 'budget wear    ronald ngara',          'forest lane    ngara',                         '1500ksh', '4.0km',  'willy masinde'),
    ('mtindo  wear',                    '726620888', 'budget wear    ronald ngara',          'grand oyester',                                '1500ksh', '7.5km',  'willy masinde'),
    ('sunrays  - flora house',          '700797110', 'sunrays  flora house  - cosmetics',    'nyayo high rise',                              '4500ksh', '7.2km',  'daniel nyakundi'),
    ('sunrays   - flora   house',       '700797110', 'sunrays  flora house  - cosmetics',    'kariakor  blue gate   court    house  no  7688','3500ksh', '1.9km',  'johnsons wawire'),
    ('noreen',                          '721999686', 'moi avenue   - mageso   chamber    mezanine', 'dtb   bank  1 & 2    in westlands',    '1500ksh', '7.4km',  'cyrus ambani'),
    ('queens  - rng plaza',             '710617679', 'queens  - rng plaza',                 'qwetu   residence   jogoo rd',                 '2000ksh', '4.5km',  'shadrack atito'),
    ('adultroom   -starmall',           '106205106', 'digital  shopping mall',              'banana  -ruaka',                               '3500ksh', '12.6km', 'tony'),
    ('adultroom   -starmall',           '106205106', 'starmall  shopping mall  -   adult room','maziwa junction -masbeth appartments',      '1800ksh', '12.0km', 'daniel nyakundi'),
    ('jazy  - capital centre',          '748747848', 'jazy  -capitla centre',               'national archives',                            '3500ksh', '5.7km',  'johnsons wawire'),
    ('nancy listers  -carwash',         '721429708', 'super metro - national archives',     'listers carwash  - kindaruma rd',              '3500ksh', '4.7km',  'cyrus ambani'),
    ('kwa mwalimu - kamukunji',         '757609903', 'kwa mwalimu kamukunji',               'yaya centre',                                  '2500ksh', '750m',   'shadrack atito'),
    ('gloria   kitchenware',            '113235433', 'gloria kitchenware',                  'imeti  house',                                 '3500ksh', '6.5km',  'johnsons wawire'),
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
