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
    'belizi': 423, 'mtindo  wear': 657, 'mtindo': 609,
    'queens': 595, 'wakiarie': 551, 'avana': 521, 'superfine': 518,
    'jazi': 583, 'jazy': 583, 'gloria': 489, 'almond': 489,
    'athiambo': 634, 'kiatu': 341, 'micheal': 604, 'michael': 604,
    'sekani': 385, 'health': 472,
    'chelsea': 452, 'alfa': 649, 'unique': 513, 'andrew': 607,
    'yvonne': 651, 'kwa brown': 652, 'alina': 655, 'nooreen': 656,
    'noreen': 656, 'norren': 656, 'queensrng': 658, 'nancy': 659,
    'kwa mwalimu': 660, 'odero': 662, 'climesh': 663, 'muna': 664,
    'home of trainer': 665, 'villa blooms': 666, 'nolans': 668,
    'lina yarn': 669, 'joy': 670, 'genuine kunga': 671, 'baddies': 632,
    'mercy': 673, 'vallaries': 674, 'nia petals': 675,
    'willy-riverside': 676, 'trainers': 677, 'rebune': 678,
    'tange': 679, 'kimathi': 680, 'nashique': 682, 'miyanne': 683,
    'fashion fix': 684,
    # new clients for july 17
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
scheduled_date = "2026-07-17"

# (client, phone, pickup, dropoff, dist, rider)
rows = [
    ('fitbox',                      '759396635', 'Kamkunji police station',          'Karen, langata road binaa',                        '15.1km', 'willy masinde'),
    ('sunrays   - flora house',     '700797110', 'sunrays   - flora house',           'Himalaya heights, kindaruma road kilimani',         '6.0km',  'johnson wawire'),
    ('sunrays   - flora house',     '700797110', 'sunrays   - flora house',           'Royal Garden, Kindaruma Rd, Nairobi',               '5.2km',  'tony sangura'),
    ('fitbox',                      '759396635', 'Kamkunji police station',           'kilimani',                                          '6.0km',  'shadrack atito'),
    ('Queens',                      '710617679', 'Rng plaza',                         'Parkfield place, muthangari drive',                 '6.5km',  'johnson wawire'),
    ('Trainers be sway',            '254140068370', 'Kamukunji Business Center',      'Limuru, brackenhurst',                              '34km',   'shadrack atito'),
    ('rand landings',               '714348056', 'rand Landings Apratment C2-8',      'Tsavo Sunset, Thindigua C401',                      '14km',   'cyrus ambani'),
    ('Adult Room',                  '254106205106', 'Adult Room, Digital Shopping Mall', 'Mirema',                                         '13km',   'willy masinde'),
    ('Health classic',              '722995300', 'nextgen mall',                      'Rayan Coach Eastleigh Ankara medical center',       '7.5km',  'tony sangura'),
    ('wakiarie business',           '742537182', 'afya center',                       'Kileleshwa',                                        '6.9km',  'daniel nyakundi'),
    ('Muna Flowers',                '724906221', 'city market',                       'Kiambu',                                            '15km',   'willy masinde'),
    ('Health classic',              '722995300', 'nextgen mall',                      'Centella Therapy & Faith Mbuya',                    '5.9km',  'tony sangura'),
    ('queenschoice',                '710617679', 'cianda mall',                       'alba aparatment',                                   '9.6km',  'johnson wawire'),
    ('halima dera fashions',        '795118132', 'cianda mall',                       '2nk parcel',                                        '350m',   'johnson wawire'),
    ('halima dera fashions',        '795118132', 'cianda mall',                       'ena coach',                                         '750m',   'johnson wawire'),
    ('halima dera fashions',        '795118132', 'cianda mall',                       'macoks',                                            '400m',   'johnson wawire'),
    ('halima dera fashions',        '795118132', 'cianda mall',                       'easy coach',                                        '1km',    'johnson wawire'),
    ('sunrays   - flora house',     '700797110', 'sunrays   - flora house',           'South B sanasana la Enzi',                          '6.1km',  'johnson wawire'),
    ('Alfa fashions',               '796736969', 'Rng plaza',                         'Makanzu lower kabete',                              '11km',   'daniel nyakundi'),
    ('Alfa fashions',               '796736969', 'Makanzu lower kabete',              'Rng plaza',                                         '11km',   'daniel nyakundi'),
    ('Adult Room',                  '106205106', 'starmall',                          'Imara park apartments',                             '12.9km', 'cyrus ambani'),
    ('joy business',                '718840856', 'Jethwa mansion',                    'Pension towers loita street cbd',                   '1.3km',  'johnson wawire'),
    ('noreen',                      '721999686', 'Eastleigh social hall f93',         'IPS building 7th Floor, office number',             '6.3km',  'tony sangura'),
    ('sunrays   - flora house',     '700797110', 'sunrays   - flora house',           'Impala Paradise, kiambu',                           '12.7km', 'willy masinde'),
    ('mtindo wear',                 '726620888', 'cianda mall',                       'hurlinghum finix casino',                           '4.2km',  'shadrack atito'),
    ('mtindo wear',                 '726620888', 'cianda mall',                       'meru raha parcel',                                  '800m',   'shadrack atito'),
    ('mtindo wear',                 '726620888', 'cianda mall',                       'nnus to naivasha',                                  '1km',    'cyrus ambani'),
    ('mtindo wear',                 '726620888', 'cianda mall',                       'simba villas embakasi',                             '14km',   'johnson wawire'),
    ('mtindo wear',                 '726620888', 'cianda mall',                       'dynamic mall',                                      '450m',   'shadrack atito'),
    ('Alfa fashions',               '796736969', 'cianda mall',                       'dul dul phase 1 godown 9',                          '12km',   'johnson wawire'),
    ('queens collection',           '710617679', 'cianda mall',                       'Kileleshwa',                                        '6.7km',  'shadrack atito'),
    ('unique collection',           '513',       'cianda mall',                       'jacaranda kayole',                                  '11km',   'johnson wawire'),
    ('andrew',                      '607',       'cianda mall',                       'kily apartments',                                   '21km',   'cyrus ambani'),
    ('halima dera fashions',        '795118132', 'cianda mall',                       'kindaruma road',                                    '5.4km',  'cyrus ambani'),
    ('sunrays   - flora house',     '700797110', 'sunrays   - flora house',           'donholm',                                           '7.5km',  'tony sangura'),
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
