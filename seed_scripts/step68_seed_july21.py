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
    'joy': 670, 'muna': 664, 'miyanne': 683, 'maynne': 683,
    'rebune': 678, 'halima': 692, 'rand landings': 693, 'lucy': 694,
    'nancy': 659, 'muthoni': 695, 'georgina': 696, 'raven': 697,
    'mystiq': 698, 'linet': 699, 'nolan': 668, 'kwa mwalimu': 660,
    'trainers': 677,
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374,
    'willy': 403, 'jesse': 109, 'daniel': 310,
    'tony': 661, 'kelvin': 667, 'kevin': 667, 'nyakundi': 310,
}

def get_id(name, mapping):
    name = str(name).lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-07-21"

# (client, phone, pickup, dropoff, dist, rider)
rows = [
    ('sunrays  cosmetics',          '700797110',    'sunrays  - flora house',               'upperhill  -  opp ack gardens',                    '3.2km',  'willy masinde'),
    ('linet',                       '727405963',    'jogoo rd',                             'the tunnel  - godown     5 ( finlay)',              '13.0km', 'shadrack atito'),
    ('rebune  international',       '711670387',    'south b',                              'eastleigh',                                        '5.8km',  'tony sangura'),
    ('rebune  international',       '711670387',    'rebune  international',                'jude valley    mount appartment',                  '17.3km', 'tony sangura'),
    ('rebune  international',       '711670387',    'rebune  international',                'kilimani - mpuuga garden',                         '6.3km',  'tony sangura'),
    ('rebune  international',       '711670387',    'rebune  international',                'cbd - jumia',                                      '5.2km',  'tony sangura'),
    ('rebune  international',       '711670387',    'kilamni  mpuuga garden',               'rebune   international',                           '6.3km',  'tony sangura'),
    ('sunrays  cosmetics',          '700797110',    'sunrays  - flora house',               'wedy court    off   david    osieli  road',         '3.7km',  'willy masinde'),
    ('adultroom  - starmall',       '106205106',    'starmall  - tommboya',                 'thindigua',                                        '10.8km', 'daniel nyakundi'),
    ('adultroom  - starmall',       '106205106',    'starmall  - tommboya',                 'ngong',                                            '23.3km', 'cyrus ambani'),
    ('adultroom  - starmall',       '106205106',    'starmall  - tommboya',                 'westpark appartments',                             '2.5km',  'cyrus ambani'),
    ('trainers  by sway',           '254140068370', 'kamukunji business centre',            'sameer business park',                             '9.8km',  'shadrack atito'),
    ('trainers  by sway',           '254140068370', 'kamukunji business centre',            'karen  -hardy',                                    '18.1km', 'shadrack atito'),
    ('wakiarie  business',          '74537181',     'wakiarie  business  - afya centre',    'username properties',                              '1.3km',  'willy masinde'),
    ('halima  - dera',              '795118132',    'cianda   mall  -fagi shop',            'sawa mall',                                        '1.6km',  'willy masinde'),
    ('halima  - dera',              '795118132',    'cianda   mall  -fagi shop',            'ena coah',                                         '750m',   'kelvin ndungu'),
    ('halima  - dera',              '795118132',    'cianda   mall  -fagi shop',            'gurdian',                                          '1.5km',  'kelvin ndungu'),
    ('halima  - dera',              '795118132',    'cianda   mall  -fagi shop',            '2nk  - gaberoone rd',                              '950m',   'kelvin ndungu'),
    ('halima  - dera',              '795118132',    'cianda   mall  -fagi shop',            'kinatwa',                                          '400m',   'kelvin ndungu'),
    ('nancy   -listers carwash',    '721429708',    'priscom computer s - moi avenue',      'listers carwash  - kindaruma rd',                  '4.8km',  'johnson wawire'),
    ('sekani  -flowers',            '',             'northside',                            'fourways',                                         '9.7km',  'cyrus ambani'),
    ('halima  - dera',              '795118132',    'cianda   mall  -fagi shop',            'plainsview south b',                               '5.8km',  'johnson wawire'),
    ('halima  - dera',              '795118132',    'cianda   mall  -fagi shop',            'dau  swahili dishes -kingara rd',                  '9.1km',  'johnson wawire'),
    ('sunrays  cosmetics',          '700797110',    'sunrays  - flora house',               'huruma   -juja b',                                 '6.4km',  'shadrack atito'),
    ('health classique',            '722995300',    'health classique',                     'bazaar biulding',                                  '6.5km',  'shadrack atito'),
    ('queens   -rng plaza',         '710617679',    'queens -rng plaza',                    'langata rubis',                                    '5.8km',  'johnson wawire'),
    ('alfa  fashions',              '796736969',    'alfa  fashiosn -rng',                  'dul dul  phase 1',                                 '14.6km', 'tony sangura'),
    ('alfa  fashions',              '796736969',    'dul dul phase 1',                      'alfa fashions',                                    '14.6km', 'tony sangura'),
    ('trainers  by sway',           '254140068370', 'kamukunji business centre',            'gituro  lane',                                     '14.4km', 'daniel nyakundi'),
    ('halima  - dera',              '795118132',    'cianda   mall  -fagi shop',            'sasa mall',                                        '1.2km',  'kelvin ndungu'),
    ('Miyanne Gifts',               '',             'tsavo sunset -thidigua',               'kagiwa  appartments',                              '14.4km', 'cyrus ambani'),
    ('athiambo -thrift',            '112012425',    'cianda   mall  -fagi shop',            'kilimani',                                         '6.0km',  'willy masinde'),
    ('athiambo -thrift',            '112012425',    'cianda   mall  -fagi shop',            'westalnd  -misty springs',                         '3.6km',  'willy masinde'),
    ('kwa mwalimu -kamukunji',      '726211167',    'kamukunji business centre',            'lower kabete',                                     '7.5km',  'johnson wawire'),
    ('trainers  by sway',           '254140068370', 'trainers  by sway',                    'westagte',                                         '6.3km',  'shadrack atito'),
    ('noreen',                      '721999686',    'royal  palms',                         'embassy  of israel    limuru',                     '6.1km',  'cyrus ambani'),
    ('andrew thrift',               '718820994',    'cianda mall',                          'south c',                                          '6.9km',  'tony sangura'),
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
