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
    'adult': 586, 'jazi': 583, 'jazzy': 583,
    'purple': 408, 'queens': 595,
    'classic': 332, 'yyvonne': 631, 'yvvonne': 631, 'yvvone': 631,
    'superfine': 518, 'supefine': 518,
    'unique': 513,
    'fitbox': 338, 'micheal': 604, 'michael': 604,
    'mtindo': 609, 'health': 472, 'helath': 472,
    'gloria': 489, 'almond': 489,
    'athiambo': 634, 'avana': 521,
    'andrew': 607,
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
scheduled_date = "2026-06-30"

rows = [
    ('Adult room  -  star mall', '106205106', 'star mall', 'evangelical  victory church', '5000ksh', '9.4km', 'jesse victor'),
    ('jazi sports wear  - capitla centre', '748747848', 'jazi  sports wear', 'nine groove - westalnds', '2500ksh', '12.6km', 'willy masinde'),
    ('purple heart   - nextgen mall', '715207744', 'purple heart  - nextgen mall', 'nita indurstrial area', '3500ksh', '4.5km', 'jesse victor'),
    ('queens  choice  - dyanmic mall', '768887510', 'queens   choice  - dynamic amll', 'five star   phase 1   estate', '1500ksh', '6.3km', 'willy masinde'),
    ('queens choice   -   dynamic mall', '768887510', 'queens  choice  - dynamic   mall', 'muthama towers  - syokimau', '1500ksh', '19.9km', 'willy masinde'),
    ('classic   cosmetics  - moyale mall', '700797110', 'classic  cosmetics  -moyale mall', 'chania genesis', '15000ksh', '5.7km', 'daniel nyakundi'),
    ('yvvonne  - jitihada', '768887510', 'yvvone  jitihada', 'westalnds', '7500ksh', '3.3km', 'johnson wawire'),
    ('supefine beddings  - shop 42', '717679016', 'superfine bedding   - shop 42', 'komarock', '2500ksh', '13.3km', 'johnson wawire'),
    ('supefine beddings  - shop 42', '717679016', 'superfine bedding   - shop 42', 'buruburu', '2500ksh', '7.4km', 'johnson wawire'),
    ('unique collections', '114626845', 'unique   collections', 'molo line  -  tea room', '7000ksh', '650m', 'jesse victor'),
    ('fitbox  kamukunji', '759396635', 'fitbox  kamukunji', 'juja', '4500ksh', '32.4km', 'johnson wawire'),
    ('micheals   -tommboya', '794775593', 'micheals  -tommboya', 'riverside', '2500ksh', '5.0km', 'cyrus ambani'),
    ('mtindo wear  - hakati', '710130388', 'super metro', 'gogo mall  - pick up mtaani', '1500ksh', '750m', 'jesse victor'),
    ('mtindo wear  - hakati', '710130388', 'gogo mall', '2nk  - gaborone   rd', '1500ksh', '900m', 'jesse victor'),
    ('mtindo wear  - hakati', '710130388', 'gogo mall', 'kinatwa parcel', '1500ksh', '900m', 'jesse victor'),
    ('mtindo wear  - hakati', '710130388', 'gogo mall', 'ruaka', '1500ksh', '15.0km', 'jesse victor'),
    ('mtindo wear  - hakati', '710130388', 'gogo mall', 'ruiru', '2500ksh', '23.8km', 'jesse victor'),
    ('classic   cosmetics  - moyale mall', '700797110', 'classic  cosmetics  -moyale mall', 'bunroma line', '1500ksh', '5.6km', 'daniel nyakundi'),
    ('health classique -nextgen mall', '722995300', 'nextgen mall', 'stanbank   house', '10000ksh', '6.5km', 'willy masinde'),
    ('health classique -nextgen mall', '722995300', 'nextgen mall', 'westlands-western hieghts', '10000ksh', '10.3km', 'willy masinde'),
    ('health classique -nextgen mall', '722995300', 'nextgen mall', 'upperhill', '10000ksh', '5.5km', 'willy masinde'),
    ('gloria  kitchenware  -  almond park  off kilifi close', '113235433', 'almond park off kilifi close', 'garden villas', '4500ksh', '12.5km', 'cyrus ambani'),
    ('athiambo thrift   - hakati', '112012425', 'athiambo   thrift   - hakati', 'chania  genesis', '1500ksh', '1.0km', 'johnson wawire'),
    ('athiambo thrift   - hakati', '112012425', 'athiambo   thrift   - hakati', 'dynamic mall', '2500ksh', '1.5km', 'johnson wawire'),
    ('supefine beddings  - shop 42', '717679016', 'superfien beddings   - shop 42', 'kangemi', '4500ksh', '13.4km', 'johnson wawire'),
    ('avana soles kariakor', '702840229', 'avana  soles kariakor', 'nicco movers  - cbd -bestlady', '4500ksh', '1.7km', 'daniel nyakundi'),
    ('andrew  -phladelphia', '701549056', 'andrew philadelphia', 'ndenderu  - kiambu', '3500ksh', '18.1km', 'cyrus ambani'),
    ('classic   cosmetics  - moyale mall', '700797110', 'classic  cosmetics  -moyale mall', 'chania genesis', '1000ksh', '1.1km', 'daniel nyakundi'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 30.06.2026")
