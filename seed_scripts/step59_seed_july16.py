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
    'queens': 595, 'wakiarie': 551, 'avana': 521, 'superfine': 518,
    'jazi': 583, 'jazy': 583, 'gloria': 489, 'almond': 489,
    'athiambo': 634, 'kiatu': 341, 'micheal': 604, 'michael': 604,
    'sekani': 385, 'health': 472,
    'chelsea': 452, 'alfa': 649, 'rng': 649, 'yvonne': 651,
    'kwa brown': 652, 'alina': 655, 'nooreen': 656, 'noreen': 656, 'norren': 656,
    'queensrng': 658, 'nancy': 659, 'kwa mwalimu': 660,
    'odero kevin': 681, 'odero': 662, 'climesh': 663, 'muna': 664,
    'home of trainer': 665, 'villa blooms': 666,
    'nolans': 668, 'lina yarn': 669, 'joy': 670,
    'genuine kunga': 671, 'baddies': 632,
    'mercy': 673, 'vallaries': 674, 'nia petals': 675,
    'willy-riverside': 676, 'trainers': 677,
    'rebune': 678, 'tange': 679, 'kimathi': 680,
    'nashique': 682, 'miyanne': 683, 'fashion fix': 684,
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
scheduled_date = "2026-07-16"

rows = [
    ('wakiarie business',               '742537182', 'afya center',                              'nairobi west hospital',                        '0ksh',   '4.0km',  'willy masinde'),
    ('norren',                          '721999686', 'njugu lane',                               'Muthaiga Mini market',                         '0ksh',   '6.2km',  'tony sangura'),
    ('Rebune international',            '711670387', 'Rebune international',                     'town nyamakima',                               '0ksh',   '4.7km',  'shadrack atito'),
    ('Rebune international',            '711670387', 'Rebune international',                     'jumia luthuli avenue',                         '0ksh',   '4.7km',  'shadrack atito'),
    ('Rebune international',            '711670387', 'Rebune international',                     'eastliegh',                                    '0ksh',   '6.1km',  'shadrack atito'),
    ('Tange collection',                '714348056', 'cianda mall room 706',                     'thindigua',                                    '0ksh',   '13km',   'johnson wawire'),
    ('Kimathi House',                   '798286199', 'Kimathi House',                            'Broadwalk mall',                               '0ksh',   '3.1km',  'cyrus ambani'),
    ('avana soles',                     '702840229', 'avana soles - -karakor market',            'ngara chambers road',                          '0ksh',   '5.1km',  'willy masinde'),
    ('avana soles',                     '702840229', 'avana soles - -karakor market',            'NHC langata',                                  '0ksh',   '9.3km',  'johnson wawire'),
    ('sunrays   - flora house',         '700797110', 'sunrays   - flora house',                  'Luqman mall, Lavington',                       '0ksh',   '7.0km',  'daniel nyakundi'),
    ('kiatu emporium',                  '733273632', 'kiatu emporium   -    mepalux',            'KICD',                                         '0ksh',   '1.9km',  'willy masinde'),
    ('kiatu emporium',                  '733273632', 'kiatu emporium   -    mepalux',            'parklands',                                    '0ksh',   '3.7km',  'shadrack atito'),
    ('odero kevin',                     '712445305', 'ministry of lands',                        'kikuyu',                                       '0ksh',   '21km',   'shadrack atito'),
    ('health classic',                  '722995300', 'Nextgen -mall',                            'Cianda House, Koinange street',                '0ksh',   '5.9km',  'johnson wawire'),
    ('sunrays   - flora house',         '700797110', 'sunrays   - flora house',                  'Upper hill, Riverside Ubery lodge',            '0ksh',   '3.4km',  'daniel nyakundi'),
    ('jazy  - capital centre',          '748747848', 'jazy  - capital centre',                   'Neris Court South B',                          '0ksh',   '1.7km',  'johnson wawire'),
    ('sunrays   - flora house',         '700797110', 'sunrays   - flora house',                  'Milimani commercial courts',                   '0ksh',   '2.7km',  'daniel nyakundi'),
    ('Trainers be sway',                '254140068370','Kamukunji Business Center',              'Theta lane, kilimani',                         '0ksh',   '6.4km',  'cyrus ambani'),
    ('mtindo wear  - cianda mall',      '726620888', 'cianda mall  - mfagano street',            'north rift parcel courier',                    '0ksh',   '800m',   'tony sangura'),
    ('mtindo wear  - cianda mall',      '726620888', 'cianda mall  - mfagano street',            'guardian parcel courier',                      '0ksh',   '1.2km',  'tony sangura'),
    ('mtindo wear  - cianda mall',      '726620888', 'cianda mall  - mfagano street',            'bus car',                                      '0ksh',   '1.1km',  'tony sangura'),
    ('mtindo wear  - cianda mall',      '726620888', 'cianda mall  - mfagano street',            '3rd parklands suswa road farmud apartment',    '0ksh',   '5.6km',  'tony sangura'),
    ('mtindo wear  - cianda mall',      '726620888', 'cianda mall  - mfagano street',            'elshadai gardens karen',                       '0ksh',   '16.2km', 'tony sangura'),
    ('Nashique',                        '798086199', 'Kimathi House house 3rd Floor, shop 303',  'Pick up mtaani Gogo Mall',                     '0ksh',   '1.5km',  'willy masinde'),
    ('Trainers be sway',                '254140068370','Theta lane, kilimani',                   'Kamukunji Business Center',                    '0ksh',   '6.4km',  'cyrus ambani'),
    ('Superfine bedding',               '717679016', 'Bestlady shop 42',                         'Wangige',                                      '0ksh',   '19.3km', 'johnson wawire'),
    ('Miyanne gifts',                   '729228868', 'City Market',                              'kitengela',                                    '0ksh',   '32.1km', 'shadrack atito'),
    ('sunrays   - flora house',         '700797110', 'sunrays   - flora house',                  'Batubatu Gardens, Flora hostel gate B',        '0ksh',   '3.5km',  'daniel nyakundi'),
    ('sunrays   - flora house',         '700797110', 'sunrays   - flora house',                  'Joy Palace and accommodation, Westlands',      '0ksh',   '4.7km',  'daniel nyakundi'),
    ('norren',                          '721999686', 'Accra Towers ,5th Floor,shop B5.',         'Greenspan phase 6',                            '0ksh',   '11.1km', 'cyrus ambani'),
    ('Fashion fix',                     '769777641', 'Greatwall Athi River block 20 house 33',   'Beijing Road bluebells apartment',             '0ksh',   '11.6km', 'shadrack atito'),
    ('Fashion fix',                     '769777641', 'Greatwall Athi River block 20 house 33',   'Syokimau(Amalia apartments)iko chaddy road',   '0ksh',   '13.9km', 'shadrack atito'),
    ('Fashion fix',                     '769777641', 'Greatwall Athi River block 20 house 33',   'south b',                                      '0ksh',   '26.1km', 'shadrack atito'),
    ('yvonne jitihada',                 '727111000', 'jitihada',                                 'Nairat Apartments Ngong',                      '0ksh',   '24km',   'tony sangura'),
    ('alvana soles',                    '702840229', 'avana soles - -karakor market',            'bus car parcel delivery service',              '0ksh',   '4.6km',  'willy masinde'),
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
