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
    'mtindo': 609, 'queens': 595, 'wakiarie': 551, 'avana': 521,
    'jazy': 583, 'jazi': 583, 'athiambo': 634, 'andrew': 607,
    'kiatu': 341, 'gloria': 489, 'almond': 489,
    'chelsea': 452, 'alfa': 649, 'rng': 649,
    'yellow pages': 650, 'yellowpages': 650,
    'yvonne': 651,
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374,
    'willy': 403, 'jesse': 109, 'daniel': 310,
}

def get_id(name, mapping):
    name = str(name).lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-07-08"

rows = [
    ('queens choice -kenya cinema',             '768887510', 'queens choice  - kenya cinema',        'pick up mtaani  - gogo mall',          '1500ksh',  '600m',     'johnson wawire'),
    ('queens choice -kenya cinema',             '768887510', 'queens choice  - kenya cinema',        'molo-line',                            '2500ksh',  '900m',     'johnson wawire'),
    ('queens choice -kenya cinema',             '768887510', 'queens choice  - kenya cinema',        'south c',                              '2500ksh',  '6.7km',    'johnson wawire'),
    ('queens choice -kenya cinema',             '768887510', 'queens choice  - kenya cinema',        'phenom   park langata',                '2500ksh',  '8.1km',    'johnson wawire'),
    ('adultroom  -   starmall',                 '106205106', 'adultroom  -starmall',                 'pangani   -magunas supermarket',       '2500ksh',  '4.1km',    'cyrus ambani'),
    ('adultroom  -   starmall',                 '106205106', 'adultroom  -starmall',                 'mukuru affordable  housing',           '1800ksh',  '8.8km',    'cyrus ambani'),
    ('rng plaza -alfa fashions',                '796736969', 'rng plaza  - alfa fashions',           'eens business park  - msa rd',         '2500ksh',  '17.6km',   'daniel nyakundi'),
    ('rng plaza -alfa fashions',                '796736969', 'rng plaza  - alfa fashions',           'langata carnivore',                    '2500ksh',  '7.1km',    'johnson wawire'),
    ('rng plaza -alfa fashions',                '796736969', 'rng plaza  - alfa fashions',           'karen  -the hub',                      '2500ksh',  '16.2km',   'cyrus ambani'),
    ('sunrays cosmetics  -flora house',         '700797110', 'sunrays   cosmetics  - flora house',   'genuine kunga therapy',                '2500ksh',  '7.2km',    'cyrus ambani'),
    ('chelsea  -new client',                    '714142519', 'starmall  - shop c1',                  'phenom   estate   house number',       '2500ksh',  '9.1km',    'johnson wawire'),
    ('mtindo wear  -  kenya cinema',            '710130388', 'mtindo  wear - kenya cinema',          'ayden plaza',                          '2500ksh',  '2.0km',    'johnson wawire'),
    ('mtindo wear  -  kenya cinema',            '710130388', 'mtindo  wear - kenya cinema',          'garden appartment  kilimani',          '4500ksh',  '5.3km',    'johnson wawire'),
    ('mtindo wear  -  kenya cinema',            '710130388', 'mtindo  wear - kenya cinema',          'fedha    residence   wanyee   road',   '2500ksh',  '10.2km',   'johnson wawire'),
    ('mtindo wear  -  kenya cinema',            '710130388', 'mtindo  wear - kenya cinema',          'grand   oyetser   appartment',         '2500ksh',  '6.5km',    'johnson wawire'),
    ('mtindo wear  -  kenya cinema',            '710130388', 'mtindo  wear - kenya cinema',          'chania sacco -river road',             '2500ksh',  '900m',     'johnson wawire'),
    ('mtindo wear  -  kenya cinema',            '710130388', 'mtindo  wear - kenya cinema',          'narrok line',                          '2500ksh',  '1.2km',    'johnson wawire'),
    ('gloria kitchenware almond park',          '707414270', 'almond park off kilifi close',         'badili appartments',                   '2500ksh',  '20.0km',   'johnson wawire'),
    ('gloria kitchenware almond park',          '707414270', 'almond park off kilifi close',         'citibank - upperhill',                 '2500ksh',  '5.3km',    'shadrack atito'),
    ('yellow  pages   -westlands',              '706829859', 'yellow pages  - westlands',            'cianda mall',                          '2500ksh',  '3.8km',    'shadrack atito'),
    ('wakiarie business',                       '742537182', 'wakiarie',                             'shauri moyo',                          '4500ksh',  '2.7km',    'shadrack atito'),
    ('avana  soles',                            '702840229', 'kariakor market',                      'pyramind square',                      '2500ksh',  '9.5km',    'shadrack atito'),
    ('avana  soles',                            '702840229', 'kariakor market',                      'happya valley  estate',                '2500ksh',  '15.5km',   'shadrack atito'),
    ('classic  cosmetics   -moyale mall',       '700797110', 'dyce beauty  store',                   'classic  comsetics  - moyale mall',    '2500ksh',  '4.1km',    'daniel nyakundi'),
    ('wakiarie  -business',                     '742537182', 'afya centre',                          'upperhill  prism   tower',             '2500ksh',  '3.2km',    'shadrack atito'),
    ('wakiarie business',                       '742537182', 'afya centre',                          'nyayo  stadium',                       '2500ksh',  '4.2km',    'johnson wawire'),
    ('athiambo   thrifts  -hakati',             '112012425', 'athiambo thrifts   -hakati',           'family court  - kirgiti',              '3000ksh',  '15.6km',   'shadrack atito'),
    ('athiambo   thrifts  -hakati',             '112012425', 'athiambo thrifts   -hakati',           'misty  springs',                       '2500ksh',  '4.7km',    'cyrus ambani'),
    ('jazy   -capital centre',                  '748747848', 'jazy  capital centre',                 'south c  - ruby flats',                '2500ksh',  '2.3km',    'willy masinde'),
    ('sunrays cosmetics  -flora house',         '700797110', 'sunrays   cosmetics  - flora house',   'mirage   towers   -westlands',         '2500ksh',  '3.8km',    'willy masinde'),
    ('sunrays cosmetics  -flora house',         '700797110', 'sunrays   cosmetics  - flora house',   'pentagon valley  - kilimani',          '2500ksh',  '6.1km',    'daniel nyakundi'),
    ('sunrays cosmetics  -flora house',         '700797110', 'sunrays   cosmetics  - flora house',   'thrive vatality   -hurlingham',        '3000ksh',  '4.2km',    'daniel nyakundi'),
    ('andrew  - cianda',                        '718820494', 'andrew - cianda',                      'fourways  - junction   kiambu rd',     '2500ksh',  '10.9km',   'shadrack atito'),
    ('kiatu emporium',                          '733273632', 'mepalux  -kiatu emporium',             'sabis  international school',          '1500ksh',  '10.8km',   'shadrack atito'),
    ('kiatu emporium',                          '733273632', 'sabis   international school',         'mepalux   -kiatu emporium',            '2500ksh',  '10.8km',   'shadrack atito'),
    ('yvonne jitihada',                         '727111000', 'jitihada shopping center',             'hatheru road',                         '3500ksh',  '10.5km',   'johnson wawire'),
    ('yvonne jitihada',                         '727111000', 'hatheru road',                         'jitihada shopping center',             '3500ksh',  '10.5km',   'johnson wawire'),
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
