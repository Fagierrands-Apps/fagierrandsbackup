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
    'superfine': 518, 'jazi': 583, 'gloria': 489, 'almond': 489,
    'athiambo': 634, 'kiatu': 341, 'micheal': 604, 'michael': 604,
    'sekani': 385, 'health': 472,
    'chelsea': 452, 'alfa': 649, 'rng': 649,
    'yvonne': 651, 'kwa brown': 652, 'nkirobi': 653,
    'alina': 655, 'nooreen': 656, 'noreen': 656,
    'queensrng': 658, 'nancy': 659, 'kwa mwalimu': 660,
    'odero': 662, 'climesh': 663, 'muna': 664,
    'home of trainer': 665, 'villa blooms': 666,
    'nolans': 668, 'lina yarn': 669, 'joy': 670,
    'genuine kunga': 671, 'baddies': 632,
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
scheduled_date = "2026-07-14"

rows = [
    ('nolans   kids  collections',              '717544455', 'sunset   boulevard    estate athiriver',   'ena coach',                                '2500ksh', '30.3km', 'shadrack atito'),
    ('nolans   kids  collections',              '717544455', 'sunset   boulevard    estate athiriver',   'pick up mtaani',                           '2500ksh', '30.3km', 'shadrack atito'),
    ('nolans   kids  collections',              '717544455', 'sunset   boulevard    estate athiriver',   '2nk shuttle',                              '2500ksh', '30.3km', 'shadrack atito'),
    ('lina yarn  -   greenhouse  -mall',        '713542093', 'greenhouse mall',                          'cosy homes  - ruaka',                      '2000ksh', '16.3km', 'tony sangura'),
    ('sekani fowers',                           '118260620', 'city market',                              'civil servants  langata',                  '3000ksh', '9.0km',  'johnson wawire'),
    ('wakiarie business',                       '742537182', 'afya centre',                              'lower kabete',                             '1500ksh', '14km',   'willy masinde'),
    ('wakiarie business',                       '742537182', 'afya centre',                              'nairobi west prison',                      '1500ksh', '6.2km',  'willy masinde'),
    ('avana soles  - kariakor',                 '712083313', 'kariakor market',                          'laibon rd   nrbi -harambee   school buruburu','800ksh', '6.8km',  'cyrus ambani'),
    ('avana soles  - kariakor',                 '712083313', 'kariakor market',                          'laibon rd   nrbi -harambee   school buruburu','500ksh', '6.8km',  'cyrus ambani'),
    ('joy business',                            '718840856', 'jinsala  rd',                              'pcea  kimbaa',                             '0ksh',   '24.9km', 'johnson wawire'),
    ('joy business',                            '718840856', 'glory safaris   -rpahta',                  'gikuni shopping centre',                   '0ksh',   '14.6km', 'johnson wawire'),
    ('health classique',                        '722995300', 'health classique',                         'bazaar   biulding   14th  floor',          '4500ksh', '6.4km',  'daniel nyakundi'),
    ('mtindo wear  - cianda mall  (fagi)',       '726620888', 'cianda mall  - mfagano street',            'lifesytle   signature',                    '1500ksh', '10.5km', 'tony sangura'),
    ('mtindo wear  - cianda mall  (fagi)',       '726620888', 'cianda mall  - mfagano street',            'riara  lane kilimani',                     '1500ksh', '8.0km',  'tony sangura'),
    ('mtindo wear  - cianda mall  (fagi)',       '726620888', 'cianda mall  - mfagano street',            'gallant mall',                             '1500ksh', '3.6km',  'tony sangura'),
    ('mtindo wear  - cianda mall  (fagi)',       '726620888', 'cianda mall  - mfagano street',            'westalnds',                                '1500ksh', '3.0km',  'tony sangura'),
    ('mtindo wear  - cianda mall  (fagi)',       '726620888', 'cianda mall  - mfagano street',            'karen elshadai  gardens',                  '1500ksh', '16.2km', 'daniel nyakundi'),
    ('mtindo wear  - cianda mall  (fagi)',       '726620888', 'cianda mall  - mfagano street',            'nuclear shuttle -nyamakima',               '1500ksh', '900m',   'daniel nyakundi'),
    ('genuine kunga therapy',                   '722604711', 'sunrays   cosmetics  -flora house',        'adams arcade',                             '3500ksh', '7.3km',  'willy masinde'),
    ('sunrays   - flora house',                 '700797110', 'sunrays   cosmetics  -flora house',        'kilimani',                                 '2500ksh', '5.4km',  'willy masinde'),
    ('sunrays   - flora house',                 '700797110', 'sunrays   cosmetics  -flora house',        'cozy  heaven - thindigua',                 '2500ksh', '12.1km', 'shadrack atito'),
    ('sunrays   - flora house',                 '700797110', 'kilimani',                                 'sunrays cosmetics',                        '2500ksh', '5.4km',  'willy masinde'),
    ('mtindo wear  - cianda mall  (fagi)',       '726620888', 'cianda mall  - mfagano street',            'pick up mtaani -gogo mall',                '1500ksh', '550m',   'kelvin  ndungu'),
    ('noreen',                                  '721999686', 'gaberonne   plaza',                        'ende vilee  phase  2',                     '2000ksh', '28.9km', 'shadrack atito'),
    ('noreen',                                  '721999686', 'towhid mall',                              'harambee sacco',                           '1500ksh', '4.7km',  'shadrack atito'),
    ('nancy',                                   '721429708', 'sunrays   cosmetics  -flora house',        'listers carwash   - kindaruma rd',         '1500ksh', '4.6km',  'willy masinde'),
    ('fitbox  - ke  -kamukunji',                '759396635', 'kamukunji  -police station',               'jomami -appartment',                       '4500ksh', '16.5km', 'cyrus ambani'),
    ('baddies   empire    -dynamic    mall',    '759535915', 'dynamic  mall',                            'shanggrilla residence',                    '1500ksh', '5.6km',  'johnson wawire'),
    ('nancy   listers carwash',                 '723662269', 'imenti house',                             'kindaruma rd',                             '2500ksh', '4.3km',  'johnson wawire'),
    ('kwa brown  - kamukunji business  centre', '706226766', 'kamukunji  busines centre',                'kayole junction',                          '1500ksh', '12.5km', 'cyrus ambani'),
    ('kwa brown  - kamukunji business  centre', '706226766', 'kyole   junction',                         'rng plaza',                                '0ksh',   '14.5km', 'cyrus ambani'),
    ('alfa  -fashions  -  rng  plaza',          '796736969', 'alfa  fashions  - rng plaza',              'upperhill  -cic   insurance   group',      '2000ksh', '3.2km',  'tony sangura'),
    ('wakiarie business',                       '742537182', 'afya centre',                              'national theater',                         '150ksh',  '3.9km',  'johnson wawire'),
    ('Michaels',                                '794775593', 'michaels',                                 'adams arcade',                             '200ksh',  '5.9km',  'johnson wawire'),
    ('sunrays   - flora house',                 '700797110', 'sunrays   cosmetics  -flora house',        'akiba court 3 south c',                    '1500ksh', '5.9km',  'tony sangura'),
    ('sunrays   - flora house',                 '700797110', 'sunrays   cosmetics  -flora house',        'upperhill kismbere rd royal garden',       '2500ksh', '4.1km',  'willy masinde'),
    ('sunrays   - flora house',                 '700797110', 'sunrays   cosmetics  -flora house',        'quickmart fedha',                          '3000ksh', '10.9km', 'tony sangura'),
    ('sunrays   - flora house',                 '700797110', 'sunrays   cosmetics  -flora house',        'kilimani',                                 '1500ksh', '5.4km',  'willy masinde'),
    ('baddies   empire    -dynamic    mall',    '759535915', 'dynamic  mall',                            'acacia court',                             '1500ksh', '8.0km',  'nyakundi'),
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
