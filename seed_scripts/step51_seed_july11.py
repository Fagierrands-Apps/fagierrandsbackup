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
    'mtindo  wear': 657, 'mtindo': 609, 'wakiarie': 551, 'avana': 521,
    'superfine': 518, 'jazi': 583, 'jazy': 583, 'gloria': 489, 'almond': 489,
    'athiambo': 634, 'andrew': 607, 'kiatu': 341, 'micheal': 604, 'michael': 604,
    'chelsea': 452, 'alfa': 649, 'rng': 649, 'yellow pages': 650,
    'yvonne': 651, 'kwa brown': 652, 'nkirobi': 653, 'ree style': 654,
    'alina': 655, 'nooreen': 656, 'noreen': 656, 'noreens': 656,
    'mtindongara': 657, 'queensrng': 658, 'nancy': 659, 'kwa mwalimu': 660,
    'odero': 662, 'climesh': 663,
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374,
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
scheduled_date = "2026-07-11"

rows = [
    ('sunryas -flora house',        '700797110', 'sunrays -flora house',                     'Kam place  opp westgaet',                          '1500ksh', '4.8km',  'willy masinde'),
    ('kiatu emporium',              '733273632', 'mepaluc plaza',                            '1st avenue   parklands',                           '1500ksh', '3.6km',  'johnson wawire'),
    ('avana   soles',               '702840229', 'avana   soles  - kariakor market',         'kahawa valley appartments',                        '1500ksh', '12.1km', 'willy masinde'),
    ('sunrays -flora house',        '700797110', 'sunrays -flora house',                     'uhuru camp-langata',                               '1500ksh', '6.6km',  'shadrack atito'),
    ('sunrays -flora house',        '700797110', 'sunrays -flora house',                     'genuine kunga therpay',                            '4500ksh', '7.2km',  'tony sangura'),
    ('noreens',                     '721999686', 'moi avenue    avenue  mageso   chambers',  'gateway appartments   - gatundu  crecent   kileleshwa','1500ksh','9.1km', 'tony sangura'),
    ('sunrays -flora house',        '700797110', 'sunrays -flora house',                     'kilimani -riara rd',                               '1500ksh', '9.8km',  'cyrus ambani'),
    ('sunrays -flora house',        '700797110', 'sunrays -flora house',                     '3rd  parklands avenue',                            '1500ksh', '4.2km',  'cyrus ambani'),
    ('sunrays -flora house',        '700797110', 'sunrays -flora house',                     'riara prestige  appartments',                      '1500ksh', '8.2km',  'cyrus ambani'),
    ('kiatu emporium - mepalux plaza','733273632','kiatu emporium',                          'runda mumwe',                                      '1500ksh', '11.8km', 'shadrack atito'),
    ('kiatu  emporium -mepalux  plaza','733273632','parklands',                              'kiatu emporium',                                   '1500ksh', '4.8km',  'johnson wawire'),
    ('athiambo',                    '112012425', 'hakati',                                   'oval parklands',                                   '1500ksh', '7.7km',  'willy masinde'),
    ('sunrays -flora house',        '700797110', 'sunrays -flora house',                     'the carnivore resturant langata',                  '1500ksh', '8.2km',  'johnson wawire'),
    ('odero',                       '',          'nextgen mall',                             'luckysummer',                                      '1500ksh', '17.8km', 'johnson wawire'),
    ('Micheals',                    '794775593', 'Michaels Tom mboya',                       'Cbd kitengela parcel super metro',                 '1500ksh', '230m',   'willy masinde'),
    ('adult room',                  '106205106', 'Digital  shopping mall',                   'Ruaka',                                            '2000ksh', '13.4km', 'tony sangura'),
    ('sunrays  -flora  house',      '700797110', 'sunrays -flora house',                     'carnivore  restaurant   langata',                  '1500ksh', '7.7km',  'johnson wawire'),
    ('climesh   designs',           '700039972', 'climesh designs -sienz plaza',             'pcea  makadara   jogoo rd',                        '2500ksh', '7.1km',  'daniel nyakundi'),
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
