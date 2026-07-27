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
    'mystiq': 698,
}

riders = {
    'shadrack': 477, 'shadrcak': 477, 'cyrus': 375, 'johnson': 374,
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
scheduled_date = "2026-07-20"

# rows 81-110 (remaining 30 orders for july 20)
rows = [
    ('nancy -listers carwash',          '',          'HH towers',                        'Lister car wash, kindaruma rd',                            '4.5km',  'johnson wawire'),
    ('nancy  -listers carwash',         '',          'platinum plaza',                   'Lister car wash, kindaruma rd',                            '4.3km',  'johnson wawire'),
    ('sunrays flora house',             '700797110', 'sunrays flora house',              'nhc langata',                                              '8.1km',  'shadrcak atito'),
    ('sunrays flora house',             '700797110', 'sunrays flora house',              'kenrail towers  - westlands',                              '6.7km',  'shadrack atito'),
    ('belizi fashions',                 '',          'iconic  bsuiness   plaza',         'jkuat towers',                                             '1.0km',  'shadrack atito'),
    ('belizi fashions',                 '',          'iconic  bsuiness   plaza',         'platinum plaza',                                           '160m',   'shadrack atito'),
    ('belizi fashions',                 '',          'iconic  bsuiness   plaza',         'dynamic mall',                                             '600m',   'shadrack atito'),
    ('belizi fashions',                 '',          'iconic  bsuiness   plaza',         'kai plaza',                                                '450m',   'shadrack atito'),
    ('belizi fashions',                 '',          'iconic  bsuiness   plaza',         'tea room',                                                 '850m',   'shadrack atito'),
    ('maynne  gifts',                   '721429708', 'city  market',                     'garden city',                                              '12.2km', 'daniel nyakundi'),
    ('halima dera',                     '795118132', 'fagi shop  - cianda mall',         'westlands gtc',                                            '3.4km',  'willy masinde'),
    ('halima dera',                     '795118132', 'fagi shop  - cianda mall',         '2nk shuttle gaebrone  (kericho)',                          '850m',   'kevin ndungu'),
    ('halima dera',                     '795118132', 'fagi shop  - cianda mall',         'ena coach',                                                '750m',   'kevin ndungu'),
    ('halima dera',                     '795118132', 'fagi shop  - cianda mall',         'tourism fund',                                             '3.3km',  'johnson wawire'),
    ('muthoni thrift',                  '',          'fagi shop  - cianda mall',         'akila  2   estste',                                        '5.4km',  'tony sangura'),
    ('muthoni thrift',                  '',          'fagi shop  - cianda mall',         'indurstrial are',                                          '9.5km',  'tony sangura'),
    ('halima dera',                     '795118132', 'fagi shop  - cianda mall',         'ena coach',                                                '750m',   'kevin ndungu'),
    ('halima dera',                     '795118132', 'fagi shop  - cianda mall',         'north rift',                                               '350m',   'kevin ndungu'),
    ('Athiambo   trifft shop',          '',          'fagi shop  - cianda mall',         'roasters',                                                 '9.6km',  'daniel nyakundi'),
    ('Athiambo   trifft shop',          '',          'fagi shop  - cianda mall',         'MIREMA',                                                   '14.4km', 'daniel nyakundi'),
    ('norren',                          '721999686', 'magic   business  centre',         'al rauf   restaurant',                                     '6.2km',  'willy masinde'),
    ('Sekani flowers',                  '',          'Northside apartments',             'eastleigh juja b',                                         '3.8km',  'shadrack atito'),
    ('trainers  by sway',               '254140068370', 'kamukunji business centre',     'royal media   serivces',                                   '5.9km',  'tony sangura'),
    ('noreen',                          '721999686', 'biashara street  2nd floor',       'west point heights -thogoto',                              '22.0km', 'willy masinde'),
    ('Geogina   idda',                  '',          'nyamakima     price   house',      'nyulia   court   -new njiru',                              '18.7km', 'cyrus ambani'),
    ('halima dera',                     '795118132', 'fagi shop  - cianda mall',         'lopha  travellers -latema rd',                             '700m',   'shadrack atito'),
    ('halima dera',                     '795118132', 'fagi shop  - cianda mall',         'state house    boys',                                      '4.4km',  'johnson wawire'),
    ('Athiambo   trifft shop',          '',          'hakati business centre',           'kings   sherwood   apprtments',                            '8.1km',  'johnson wawire'),
    ('raven',                           '',          'cj -koinange rd',                  'shepher pub   ruiru',                                      '26.0km', 'shadrack atito'),
    ('mystiq   petals',                 '',          'mystiq  petals -  city market',    'sted afric appartments',                                   '26.2km', 'cyrus ambani'),
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
