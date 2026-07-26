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
        s = km_str.lower().strip()
        if not s or s in ('okm','0km'): return 200
        km = float(s.replace('km','').strip()) if 'km' in s else float(s.replace('m','').strip()) / 1000
        return 200 if km <= 7.5 else round(200 + (km - 7.5) * 23)
    except:
        return 200

def parse_value(v):
    try:
        return float(''.join(c for c in v if c.isdigit() or c == '.'))
    except:
        return 0

def parse_km(s):
    try:
        s = s.lower().strip()
        if not s or s in ('okm','0km'): return 0
        return float(s.replace('km','').strip()) if 'km' in s else round(float(s.replace('m','').strip()) / 1000, 3)
    except:
        return 0

clients = {
    'gloria': 489, 'glory': 489,
    'phyliss': 481,
    'classic': 332,
    'epic': 638,
    'micheal': 604, 'michael': 604,
    'muna': 488,
    'mtindo': 609,
    'sunrays': 372, 'sunray': 372,
    'hakati': 641,
    'purple': 408,
    'irene': 528, 'bestlady': 528,
    'joy': 462,
    'wakiar': 551,
    'aoko': 599,
    'luxe': 406,
    'health': 472, 'helath': 472,
    'dyaminc': 637,
    'athiambo': 634,
    'unique fashions': 644, 'uniquefashion': 644,
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374,
    'willy': 403, 'jesse': 109, 'daniel': 310,
}

def get_id(name, mapping):
    name = name.lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-06-24"

rows = [
    ('gloria kitchenwear -almond', '707414270', 'gloria kitchenwear- almond park', 'greenvale apartment , ring road kileleshwa', '2500ksh', '8.5km', 'shadrack atito'),
    ('gloria kitchenwear', '707414270', 'gloria kitchenwear- almond park', 'munae street opposite asif house ngara', '3500ksh', '8.5km', 'shadrack atito'),
    ('gloria kitchenwear', '707414270', 'gloria kitchenwear- almond park', 'mukuyu RD', '1500ksh', '19.5km', 'shadrack atito'),
    ('phyliss  flowers  - city market', '791418630', 'phyliss  flowers  - city market', 'eastleigh', '2000ksh', '6.5km', 'jesse   victor'),
    ('classic cosmetics', '722995300', 'classic cosmetics', 'buscar', '10000ksh', '5.3km', 'daniel nyakundi'),
    ('epic human hair  -accra towers', '118544626', 'epic  human hair   -accra towers', 'biashara plaza', '45000ksh', '900m', 'daniel nyakundi'),
    ('micheal  - tommboya', '794775593', 'micheals-tommboya', 'upperhill', '2500ksh', '3.0km', 'johnson wawire'),
    ('muna  flowers   -  tubman road', '724906221', 'muna flowers  -tubman road', 'springs   jubilee   vocational  traning college', '2500ksh', '14.9km', 'willy masinde'),
    ('mtindo wear --budget wear', '729620888', 'mtindo wear   -budget wear', 'kilimani', '1500ksh', '4.5km', 'johnson wawire'),
    ('mtindo wear --budget wear', '729620888', 'mtindo wear   -budget wear', 'mucatha', '1500ksh', '15.1km', 'johnson wawire'),
    ('mtindo wear --budget wear', '729620888', 'mtindo wear   -budget wear', 'pickup  - mtaani- gogo mall', '1500ksh', '1.6km', 'johnson wawire'),
    ('mtindo wear --budget wear', '729620888', 'mtindo wear   -budget wear', 'northrift    parcels', '1500ksh', '1.5km', 'johnson wawire'),
    ('mtindo wear --budget wear', '729620888', 'mtindo wear   -budget wear', 'buscar  -charles  rubia  rd', '1500ksh', '1.0km', 'johnson wawire'),
    ('sunrays   - flora  house', '700797110', 'sunrays flora house', 'genuine  kunga   therapy', '2500ksh', '7.2km', 'jesse   victor'),
    ('hakati   bsuiness   centre', '112012425', 'hakati business  centre', '2nk parcel', '1500ksh', '1.1km', 'cyrus ambani'),
    ('purple hearts  - nexrgen mall', '700276582', 'nextgen mall', 'the piano  - brookside drive', '3500ksh', '10.1km', 'shadrack atito'),
    ('irene  bestlady', '716060029', 'irene  bestlady', 'ruai', '2500ksh', '25.5km', 'willy masinde'),
    ('joy business', '722456267', 'eastleigh- bangkok', 'cbd', '5000ksh', '6.5km', 'jesse   victor'),
    ('joy business', '722456267', 'cbd', 'westlandas  -raphta    rd', '10000ksh', '2.7km', 'jesse   victor'),
    ('wakiarie  business', '742537182', 'afya centre', 'kamiti corner mumbi mugumoini', '5000ksh', '23km', 'johnson wawire'),
    ('mtindo wear', '710130388', 'buruburu  - junction', 'super metro', '1500ksh', '7.8km', 'cyrus ambani'),
    ('aoko  bags', '729096365', 'supermetro - national archives', 'dynamic mall', '2500ksh', '270m', 'shadrack atito'),
    ('wakiaria business', '742537182', 'afya centre', 'jkuat towers', '3500ksh', '2.2km', 'shadrack atito'),
    ('luxe bags', '729096365', 'khoja  stage', 'dynamic mall', '2500ksh', '700m', 'shadrack atito'),
    ('helath classique   - nextgen', '722995300', 'health classique   -nextgen', 'trm  - getrude   hospital', '20000ksh', '17.3km', 'willy masinde'),
    ('dyaminc  - mall  -queens choice', '', 'dyanmic mall', 'purvi   house -westalnds', '1500ksh', '4.4km', 'cyrus ambani'),
    ('athiambo thrift-hakati', '1120112425', 'athiambo thrift  - hakati', 'duchess  park  - hatheru rd', '2500ksh', '10.5km', 'shadrack atito'),
    ('mtindo wear  -kitengela', '710130388', 'super metro  -national archives', 'afya   centre', '1500ksh', '450m', 'cyrus ambani'),
    ('mtindo wear-kitengela', '710130388', 'super metro  -national archives', 'northrift    parcels', '1500ksh', '650m', 'cyrus ambani'),
    ('sunrays   - flora  house', '700797110', 'sunrays flora house', 'kpa flats  - south c', '2500ksh', '8.9km', 'jesse   victor'),
    ('unique fashions', '757609903', 'unique fashions -kamukunji', 'kayole', '1500ksh', '12.0km', 'jesse   victor'),
    ('classic cosmetics', '722995300', 'dyce beauty store', 'classic  cosmetics', '15000ksh', '4.7km', 'daniel  nyakundi'),
]

success, skipped = 0, 0
for client, phone, pickup, dropoff, value, dist, rider in rows:
    client_id = get_id(client, clients)
    rider_id = get_id(rider, riders)
    if not client_id or not rider_id:
        print(f"SKIP: client='{client}' rider='{rider}'")
        skipped += 1
        continue
    price = calc_price(dist)
    est_val = parse_value(value)
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
            {km}, true, {est_val}
        ) RETURNING id, client_id, assistant_id, price, estimated_value;
    """)
    success += 1

print(f"\nDone: {success} inserted, {skipped} skipped for 24.06.2026")
