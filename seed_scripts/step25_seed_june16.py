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
        if s in ('okm', '0km', ''): return 200
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
        if s in ('okm', '0km', ''): return 0
        return float(s.replace('km','').strip()) if 'km' in s else round(float(s.replace('m','').strip()) / 1000, 3)
    except:
        return 0

clients = {
    'yyvonne': 631, 'yyvone': 631, 'jitihada': 631,
    'joy': 462, 'jazy': 583, 'jazi': 583,
    'belizi': 423, 'kiatu': 341, 'classic': 332,
    'health': 472, 'fitbox': 338, 'sunray': 372, 'sunrays': 372,
    'queen africa': 603, 'micheal': 604, 'michael': 604,
    'athiambo': 634,
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
scheduled_date = "2026-06-16"

rows = [
    ('yyvonne   -jitihada', '794447655', 'yyvonne  - jitihada', 'rocks appartment', '9000ksh', '16.9km', 'johnson wawire'),
    ('joy busieness', '718840856', 'glory safaris rphta rd', 'gillhouse-cbd', '3000ksh', '6.7km', 'willy masinde'),
    ('jazy sportwear', '748747848', 'capital centre', 'la mada hotel', '', '13.5km', 'johnson wawire'),
    ('belizi fashions', '746199107', 'noble park appartments', 'lavender heights- mirema', '3000ksh', '14.7km', 'shadrack atito'),
    ('kiatu  emporium  -mepalux', '733273632', 'kiatu empoirum-mepalux', 'james gichuru -164', '1500ksh', '8.7km', 'cyrus ambani'),
    ('classic cosmetics', '721420878', 'classic cosmetics', 'narok  line  - nyamakima', '5000ksh', '5.1km', 'daniel nyakundi'),
    ('classic cosmetics', '721420878', 'narok line -nyamakima', 'rembo  shuttle', '2500ksh', '500m', 'daniel nyakundi'),
    ('health classique', '722995300', 'health classique', 'jairo appartments', '5000ksh', '15.9km', 'shadrack atito'),
    ('fitbox  - ke', '759396635', 'fitbox -ke', 'equity mlolongo', '3000ksh', '21.0km', 'willy masinde'),
    ('fitbox  - ke', '759396635', 'equity -mlolongo', 'fitbox-ke', '3000ksh', '21.0km', 'willy masinde'),
    ('sunray  -flora house', '700797110', 'sunrays  flora house', 'perida business centre', '1500ksh', '0km', 'cyrus ambani'),
    ('sunray  -flora house', '700797110', 'perida  business centre', 'garden city  mall', '1000ksh', '10.4km', 'cyrus ambani'),
    ('queen africa -thrift', '716915247', 'delight carwash  - utawala', 'pick up mtaani  - gogo mall', '1500ksh', '25.3km', 'shadrack atito'),
    ('micheal  -tom mboya', '794775593', 'michael - tom mboya', 'south c -rangers', '2500ksh', '7.5km', 'johnson wawire'),
    ('classic cosmetics', '721420878', 'buscar', 'classic   cosmetics', '1500ksh', '3.9km', 'jesse victor'),
    ('classic cosmetics', '721420878', 'classic cosmetics', 'buscar', '2500ksh', '3.9km', 'daniel nyakundi'),
    ('queen africa -thrift', '716915247', 'queen africa  -thrift', 'garden city  mall- blue valley appartment', '1500ksh', '10.4km', 'shadrack atito'),
    ('sunray  -flora house', '700797110', 'sunrays  flora house', 'eastleight  1st avenue   ,7th street  presitige biulding', '1400ksh', '3.5km', 'jesse victor'),
    ('classic cosmetics', '721420878', 'dyce beauty store', 'classic   cosmetics', '5000ksh', '4.1km', 'daniel nyakundi'),
    ('athiambo  - thrift -hakati business', '112012425', 'athiambo thrift  -hakati   business', 'rb slates   appartments  - kiambu', '1500ksh', '14.6km', 'cyrus ambani'),
    ('classic cosmetics', '721420878', 'classic cosmetics', 'afya  centre', '5000ksh', '4.8km', 'jesse victor'),
    ('jazy sportwear', '748747848', 'capital centre  - jazu sportwear', 'kasarni sportview   estate', '1500ksh', '19km', 'jesse victor'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 16.06.2026")
