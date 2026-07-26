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
    'belizi': 423, 'mtindo': 609, 'queens': 595, 'wakiarie': 551,
    'avana': 521, 'superfine': 518, 'supefine': 518,
    'jazi': 583, 'jazy': 583, 'purple': 408,
    'yyvonne': 631, 'yvvonne': 631, 'yyvone': 631,
    'unique': 513, 'micheal': 604, 'michael': 604,
    'health': 472, 'gloria': 489, 'almond': 489,
    'athiambo': 634, 'andrew': 607, 'sekani': 385, 'kiatu': 341,
    'chelsea': 452, 'alfa': 649, 'rng': 649,
    'yellow pages': 650, 'yvonne': 651,
    'cyrus ambani': 551,  # data entry error - maps to wakiarie by phone
    'kwa brown': 652, 'nkirobi': 653, 'ree style': 654,
    'alina': 655, 'nooreen': 656, 'noreen': 656,
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
scheduled_date = "2026-07-09"

rows = [
    ('cyrus ambani',                            '742537182', 'afya centre',                          'upperhill polytechnic',                    '3500ksh', '2.9km',  'shadrack atito'),
    ('yyvone  - jitihada',                      '727111000', 'yyvonne  - jitihada',                  'kilimani',                                 '1500ksh', '5.6km',  'johnson wawire'),
    ('kwa brown  -  kamukunji',                 '706226766', 'kamukunji  trade centre',              'pipeline',                                 '2500ksh', '14.0km', 'willy masinde'),
    ('nkirobi  - new client',                   '720348793', 'kamukunji business centre',            'format village    estate   makidni rd',    '2000ksh', '8.7km',  'willy masinde'),
    ('sunrays flora -house',                    '700797110', 'sunrays flora -house',                 'jam street  - eastleigh',                  '4500ksh', '3.7km',  'shadrack atito'),
    ('health classique -nextgen',               '722995300', 'health classique   -nextgen',          'rayan coach  -  eastleigh',                '3500ksh', '8.7km',  'cyrus ambani'),
    ('alfa fashions - rng',                     '796736969', 'alfa fashions -rng plaza',             'light   international school',             '1500ksh', '14.5km', 'shadrack atito'),
    ('sunrays flora -house',                    '700797110', 'sunrays flora -house',                 '239 owashika  house , lavington',          '1500ksh', '9.2km',  'shadrack atito'),
    ('yyvonne - jitihada',                      '727111000', 'yyvonne  - jitihada',                  'kiamumbi',                                 '2000ksh', '17.6km', 'daniel nyakundi'),
    ('andrew-cianda',                           '718820494', 'andrew-cianda',                        'muthangari',                               '2600ksh', '7.0km',  'cyrus ambani'),
    ('jazi sport wear   -capital centre',       '748747848', 'capital centre',                       'shibam supplies   , baricho  road',        '1500ksh', '3.2km',  'willy masinde'),
    ('sunrays flora -house',                    '700797110', 'sunrays flora -house',                 'daylight appartments    parklands',        '2000ksh', '5.9km',  'cyrus ambani'),
    ('sunrays flora -house',                    '700797110', 'sunrays flora -house',                 'alina   ridge   ,kileleshwa    , oloitotok  rd', '1800ksh', '5.5km', 'cyrus ambani'),
    ('jazi sport wear   -capital centre',       '748747848', 'capital centre',                       'jeevan  baharati  biulding   , harambee avenue', '1700ksh', '5.7km', 'shadrack atito'),
    ('super fine beddings  - bestlady  shop 42','717679016', 'super  fine   bedding   - bestlady',   'kawangware',                               '2500ksh', '10.9km', 'willy masinde'),
    ('gloria -kitchenware almond park',         '113235433', 'almond park -kilif close',             'carlton apprtments  -mraro rd',            '4500ksh', '12.2km', 'shadrack atito'),
    ('gloria -kitchenware almond park',         '113235433', 'almond park -kilif close',             'kings kids village',                       '2300ksh', '16.4km', 'shadrack atito'),
    ('yyvonne   -jitahda',                      '727111000', 'yyvonne  - jitihada',                  'kiliamni  manelik  rd',                    '7500ksh', '6.3km',  'willy masinde'),
    ('sunrays flora -house',                    '700797110', 'fagi  - pick up mfagano street',       'gathima court   , aprk rd',                '1500ksh', '2.9km',  'daniel nyakundi'),
    ('ree style   ke',                          '799564394', 'fagi  - pick up mfagano street',       'cool -kombani',                            '1500ksh', '1.2km',  'cyrus ambani'),
    ('alfa fashions - rng',                     '796736969', 'alfa fashions -rng plaza',             '360 appartments   -katani rd',             '1500ksh', '19.9km', 'johnson wawire'),
    ('alina  - alina rdge    kileleshwa',       '791246003', 'alina ridge -kileleshwa',              'super metro  - national archives',         '3000ksh', '5.2km',  'cyrus ambani'),
    ('sunrays flora -house',                    '700797110', 'fagi pick up point   mfagano street',  'ngara    kenya police',                    '1500ksh', '1.9km',  'cyrus ambani'),
    ('micheals -tommboya',                      '794775593', 'micheals  - tommboya',                 'uganda -high commision',                   '2500ksh', '5.7km',  'johnson wawire'),
    ('classic cosmetics   - moyale mall',       '700797110', 'duboise -beauty stalls',               'classic comsetics  - moyale mall',         '10000ksh','4.1km',  'daniel nyakundi'),
    ('sunrays flora -house',                    '700797110', 'sunrays flora -house',                 'naivas -umoja',                            '2500ksh', '10.1km', 'cyrus ambani'),
    ('nooreen',                                 '721999686', 'bihi towers suite 2',                  'enden vile phase 1',                       '10000ksh','27.0km', 'shadrack atito'),
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
